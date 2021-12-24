# BigQuery query - bqq

Simple BigQuery CLI:

- show info about
  - billed project
  - cost
  - size 
- provide search history of past results

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
  -h, --history        Search history
  -d, --delete         Delete job from history
  -i, --info           Show gcloud configuration
  --clear              Clear history
  --sync               Sync history from cloud
  --help               Show this message and exit.
```

## Examples

```bash
bqq "SELECT repository.url, repository.created_at FROM bigquery-public-data.samples.github_nested LIMIT 100"
Billing project = my-google-project
Estimated size = 150.3 MiB
Estimated cost = +0.00 $
Do you want to continue? [y/N]: y
```

```bash
bqq -f query.sql
```
