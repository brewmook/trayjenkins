Description
-----------

Trayjenkins is (going to be) a simple tool to monitor Jenkins
installations.

Dependencies
------------

* Python 2.6 or later. Not tested on 3.x yet.

* [PySide](http://www.pyside.org/), version 1.0.7 or later (though
  earlier versions may work too, they just haven't been tried).

Running
-------

After cloning the repository you have to set up the git submodules:

    $ git submodule init
    $ git submodule update

On Windows, run `trayjenkins.bat`, assuming python is on your system
`PATH`.

On Linux, Mac etc, use `trayjenkins.sh`.

Licence
-------

So far, public domain, use at your own risk. A more appropriate
licence will be chosen soon.

Developer setup
---------------

When running from a Python IDE, make sure that `submodules/pyjenkins`
is added to `PYTHONPATH`.
