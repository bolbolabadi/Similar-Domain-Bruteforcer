# Similar Domain Bruteforcer

This script generates and resolves similar domain names based on a provided domain keyword. It can use TLD and compound name lists to generate domain combinations and check for active domains via DNS resolution.

## Requirements

Make sure you have the following installed:

- Python 3.x
- `massdns` (or another DNS resolver)
- Required Python packages (listed below)

## Installation

Clone this repository:

```bash
git clone https://github.com/yourusername/similar-domain-bruteforcer.git
cd similar-domain-bruteforcer
## Usage

To run the script, use the following command:

```bash
python domain_bruteforcer.py -d google -t tlds.txt -c compound_names.txt -r resolver.txt
