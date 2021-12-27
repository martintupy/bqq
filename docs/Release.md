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
twine upload --repository testpypi dist/*
```

## Test install

```bash
 python3 -m pip install --index-url https://test.pypi.org/simple/ bqq
```


## Upload 

```bash
twine upload dist/*
```