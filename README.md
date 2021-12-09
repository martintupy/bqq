# BigQuery query - bqq

Simple BigQuery CLI:
 - print estimated size and cost of query
 - cache results

### Instalation

1. `git clone https://github.com/martintupy/bqq && cd bqq`
2. `pip install --compile --user .`
3. `sh init.sh`
4. `Add local bin to $PATH`
    - In .zshrc / .bashrc add this path `"$(python -m site --user-base)/bin"`


```Bash
Usage: bqq [OPTIONS] [SQL]

  BiqQuery query.

Options:
  -f, --file FILENAME  File containing SQL
  -y, --yes            Automatic yes to prompt
  --help               Show this message and exit.
```

## Examples

```bash
bqq "SELECT repository.url, repository.created_at FROM bigquery-public-data.samples.github_nested LIMIT 100"
Estimated size: 150.3MiB
Do you want to continue? [y/N]:
```

```bash
bqq -f query.sql
```
