# Release

## 1. Build
```bash
python3 -m build
```

## 2. Check 

```bash
twine check dist/*
```

## 3. Test upload 

```bash
twine upload --repository testpypi dist/*
```

## 4. Test install

```bash
 python3 -m pip install --index-url https://test.pypi.org/simple/ bqq
```


## 5. Upload 

```bash
twine upload dist/*
```