# PerkeLE

perkeLE is a fully manual [Let's Encrypt](https://letsencrypt.org)/[ACME](https://github.com/ietf-wg-acme/acme/) client for advanced users. It is intended to be used by a human in a manual workflow and contains no automation features whatsoever.
perkeLE is a fork of [ManuaLE](https://github.com/veeti/manuale/). ManuaLE is greate command line script by Veeti Paananen with beautiful code.

## Why?

Isn't the point of Let's Encrypt to be automatic and seamless? Maybe, but here's some reasons:

* You're not comfortable with an automatic process handling something as critical, or your complex infrastructure doesn't allow it in the first place.

* You already have perfect configuration management with something like Ansible. Renewing is a matter of dropping in a new certificate. With a manual client that works, it's literally a minute of work.

* You want the traditional and authentic SSL installation experience of copying files you don't understand to your server, searching for configuration instructions and praying that it works.

## Features

* Simple interface with no hoops to jump through. Keys and certificate signing requests are automatically generated: no more cryptic OpenSSL one-liners. (However, you do need to know what to do with generated certificates and keys yourself!)

* **New in perkeLE** Support for HTTP validation. (In fact, that's the only validation method supported).

* Authorization is separate from certificate issuance. Authorizations last for months on Let's Encrypt: there's no need to waste time validating the domain every time you renew the certificate.

* **New in perkeLE** The authorization can be divided into two parts - get authorization, and check validation. You can distribute verification files manualy.

* Obviously, runs without root access. Use it from any machine you want, it doesn't care. Internet connection recommended.

* Awful, undiscoverable name.

* And finally, if the `openssl` binary is your spirit animal after all, you can still bring your own keys and/or CSR's. Everybody wins.

![simple security](perkele.png)

## Installation

### From the git repository with python

    git clone https://github.com/schors/perkele ~/
    cd ~/perkele
    python3 -m venv env
    env/bin/python setup.py install
    ln -s env/bin/manuale ~/.bin/

Assuming you have a `~/.bin/` directory in your `$PATH`.

### From the git repository with pip

    pip install --user https://github.com/schors/perkele/archive/master.zip
    ln -s ~/.local/bin/perkele ~/.bin/

Assuming you have a `~/.bin/` directory in your `$PATH`.

## Quick start

Register an account (once):

    $ perkele register me@example.com

Authorize one or more domains:

    $ perkele authorize example.com

Get your certificate:

    $ perkele issue --output certs/ example.com

Set yourself a [reminder for renewal](https://github.com/szepeviktor/debian-server-tools/blob/master/monitoring/cert-expiry.sh)!

There's plenty of documentation inside each command. Run `perkele -h` for a list of commands and `perkele [command] -h` for details.

## See also

* [Greate acme client manuaLE](https://github.com/veeti/manuale/)
* [Best practices for server configuration](https://wiki.mozilla.org/Security/Server_Side_TLS)
* [Configuration generator for common servers](https://mozilla.github.io/server-side-tls/ssl-config-generator/)
* [Test your server](https://www.ssllabs.com/ssltest/)
* [Other clients](https://community.letsencrypt.org/t/list-of-client-implementations/2103)

## DONATE

For fire, lightnings and nuts

* [Yandex.Money: 41001140237324](https://money.yandex.ru/embed/shop.xml?account=41001140237324&quickpay=shop&payment-type-choice=on&writer=seller&targets=donate+fo+perkeLE&default-sum=1000&button-text=04&successURL=)
* PayPal: `schors@gmail.com`

## TODO

* ~~Use 'Retry-After' Header for challenge rerties delay~~
* Write helps on exclusive futures
* Multilevel logging
* Remake acme.send_post method for `directory` support
* Create "JWK" package
* Import/Export account config in some other clients
* Both HTTP and DNS authorization support
* Implement call external scripts
* Allow `crypto` package for RSA512 and other

--

[![LICENSE WTFPL](wtfpl-badge-1.png)](LICENSE)
