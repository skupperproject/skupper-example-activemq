# About skewer

This repo uses [skewer](https://github.com/skupperproject/skewer) to:

* automate testing of this example
* generate the [README.md](README.md)

## Using skewer

To use skewer, you must install [plano](https://github.com/ssorj/plano) (included in this repo):

```
cd subrepos/skewer/subrepos/plano
make
make install
```

You can then test the example using the following command:
```
plano test
```
Note that this runs the example in a minikube profile, named `skewer` and deletes this profile after completing.

You can regenerate the `README.md` using the following command:
```
plano generate
```

## Dependencies

To update skewer from https://github.com/skupperproject/skewer:

```
git subrepo pull subrepos/skewer
```

Note that this command requires https://github.com/ingydotnet/git-subrepo

