# BigQuery query - bqq

Simple BigQuery CLI:

- show info about
  - billed project
  - cost
  - size 
- provide search history of past cached results

### Requirements

- fzf - https://github.com/junegunn/fzf
- gcloud - https://cloud.google.com/sdk/docs/install

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
  --dates              Search results from past execution dates
  --queries            Search results from past queries
  --clear              Clear all past results
  --help               Show this message and exit.
```

## Examples

```bash
bqq "SELECT repository.url, repository.created_at FROM bigquery-public-data.samples.github_nested LIMIT 100"
+-------------------+----------------+----------------+
|   Billed project  | Estimated cost | Estimated size |
+-------------------+----------------+----------------+
| my_google_project |      $0.0      |    157.6MB     |
+-------------------+----------------+----------------+
Do you want to continue? [y/N]: y
```

```bash
bqq -f query.sql
```
