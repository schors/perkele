"""
The domain authorization command. Authorizations last up to 300 days on the
production Let's Encrypt service at the time of writing, so it makes sense to
separate certificate issuance from ownership verification.
"""

import logging
import time
import hashlib
import json
import os

from .acme import Acme
from .crypto import generate_jwk_thumbprint, jose_b64
from .errors import ManualeError, AcmeError
from .helpers import confirm

logger = logging.getLogger(__name__)

def webroot(server, account, domains, path):
    directory = os.path.abspath(os.path.expanduser(path) + "/.well-known/acme-challenge")
    os.makedirs(directory, exist_ok=True)
    acme = Acme(server, account)
    answer = authorize(server, account, domains, acme=acme)
    authz = json.loads(answer)
    for domain in authz:
        # Write tokens
        auth = authz[domain]
        with open("{}/{}".format(directory, auth['token']), 'wb') as f:
            f.write(auth['key'].encode('utf-8'))
        logger.info("echo \"{}\"> {}/{}".format(auth['key'],directory, auth['token']))
    ready(server, account, answer.encode('utf-8'), acme=acme)
    for domain in authz:
        auth = authz[domain]
        os.unlink("{}/{}".format(directory, auth['token']))

def authorize(server, account, domains, acme=None):
    if not acme:
        acme = Acme(server, account)
    thumbprint = generate_jwk_thumbprint(account.key)

    try:
        # Get pending authorizations for each domain
        authz = {}
        for domain in domains:
            logger.info("Requesting challenge for {}.".format(domain))
            created = acme.new_authorization(domain)
            auth = created.contents
            auth['uri'] = created.uri

            # Find the HTTP challenge
            try:
                auth['challenge'] = [ch for ch in auth.get('challenges', []) if ch.get('type') == 'http-01'][0]
            except IndexError:
                raise ManualeError("Perkele only supports the http-01 challenge. The server did not return one.")

            auth['key_authorization'] = "{}.{}".format(auth['challenge'].get('token'), thumbprint)
            auth['token'] = auth['challenge'].get('token')

            authz[domain] = auth

        logger.info("")
        logger.info("HTTP verification required. Make sure these token are in place:")
        logger.info("")
        packet = {}
        for domain in domains:
            auth = authz[domain]
            logger.info("echo  \"{}\" > .well-known/acme-challenge/{} # {} {}".format(auth['key_authorization'], auth['token'], domain, auth['uri']))
            packet.update( {domain:{'token':auth['token'], 'key':auth['key_authorization'], 'uri': auth['challenge']['uri']}})
        logger.info("")
        return json.dumps(packet, indent=1,sort_keys=True, separators=(',', ':'))
    except IOError as e:
        logger.error("A connection or service error occurred. Aborting.")
        raise ManualeError(e)

def ready(server, account, authz_string, acme=None):
    if not acme:
        acme = Acme(server, account)

    try:
        # Verify each domain
        done, failed = set(), set()
        authz = json.loads(authz_string.decode('utf-8'))
        for domain in authz:
            logger.info("")
            auth = authz[domain]
            acme.validate_authorization(auth['uri'], 'http-01', auth['key'])

            retry = 5
            while True:
                logger.info("{}: waiting for verification. Checking in {} seconds.".format(domain,retry))
                time.sleep(retry)

                retry, response = acme.get_authorization(auth['uri'])
                status = response.get('status')
                if status == 'valid':
                    done.add(domain)
                    logger.info("{}: OK! Authorization lasts until {}.".format(domain, response.get('expires', '(not provided)')))
                    break
                elif status != 'pending':
                    failed.add(domain)

                    # Failed, dig up details
                    error_type, error_reason = "unknown", "N/A"
                    try:
                        challenge = [ch for ch in response.get('challenges', []) if ch.get('type') == 'http-01'][0]
                        error_type = challenge.get('error').get('type')
                        error_reason = challenge.get('error').get('detail')
                    except (ValueError, IndexError, AttributeError, TypeError):
                        pass

                    logger.info("{}: {} ({})".format(domain, error_reason, error_type))
                    break

        logger.info("")
        if failed:
            logger.info("{} domain(s) authorized, {} failed.".format(len(done), len(failed)))
            logger.info("Authorized: {}".format(' '.join(done) or "N/A"))
            logger.info("Failed: {}".format(' '.join(failed)))
        else:
            logger.info("{} domain(s) authorized. Let's Encrypt!".format(len(done)))
    except IOError as e:
        logger.error("A connection or service error occurred. Aborting.")
        raise ManualeError(e)
