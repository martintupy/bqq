# Release

## Build
```bash
python3 -m build
```

## Check 

```bash
twine check dist/*
```

## Test upload 

```bash
twine upload -r testpypi dist/*
```


## Upload 

```bash
twine upload dist/*
```