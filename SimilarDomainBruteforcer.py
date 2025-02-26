import argparse
import os
import subprocess
import threading
import logging

def setup_logging():
    logging.basicConfig(
        filename='SimilarDomainBruteforcer.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def read_file(file_path, strip_dot=False):
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return []
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        if strip_dot:
            lines = [line.lstrip('.') for line in lines]  # Remove leading dot from TLDs
        return lines

def generate_domains(domain_keyword, tlds, compounds):
    domains = set()
    for tld in tlds:
        domains.add(f"{domain_keyword}.{tld}")
        for word in compounds:
            domains.add(f"{domain_keyword}{word}.{tld}")
            domains.add(f"{word}{domain_keyword}.{tld}")
    return list(domains)

def resolve_domains(domains, resolver_file, output_file):
    input_file = f"{output_file.replace('-results.txt', '-generated.txt')}"
    
    with open(input_file, "w") as f:
        f.write('\n'.join(domains) + '\n')
    
    resolver_cmd = ["massdns", "-r", resolver_file, "-o", "S", "-w", output_file, input_file]
    subprocess.run(resolver_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    active_domains = set()
    with open(output_file, "r") as f:
        for line in f.readlines():
            domain = line.split()[0]
            domain = domain.rstrip('.')  # Strip trailing dot
            active_domains.add(domain)
    
    
    # Sort the domains alphabetically
    sorted_domains = sorted(active_domains)
    
    for domain in sorted_domains:
        logging.info(f"Active domain: {domain}")
        print(domain)
    
    return active_domains

def worker(domain_keyword, tld_file, compound_file, resolver_file):
    logging.info("Starting Similar Domain Bruteforcer")
    
    tlds = read_file(tld_file, strip_dot=True)  # Ensure TLDs are formatted correctly
    compounds = read_file(compound_file)
    domains = generate_domains(domain_keyword, tlds, compounds)
    
    logging.info(f"Generated {len(domains)} potential domains")
    
    output_file = f"{domain_keyword}-results.txt"
    active_domains = resolve_domains(domains, resolver_file, output_file)
    
    logging.info(f"Found {len(active_domains)} active domains")
    logging.info("Process completed")

def main():
    parser = argparse.ArgumentParser(description="Similar Domain Bruteforcer: Generate and resolve similar domains.")
    parser.add_argument("-d", "--domain", required=True, help="Domain keyword to use (e.g., google)")
    parser.add_argument("-t", "--tlds", required=True, help="Path to tld.txt")
    parser.add_argument("-c", "--compounds", required=True, help="Path to compound_names.txt")
    parser.add_argument("-r", "--resolver", required=True, help="Path to resolver.txt for dns resolution")
    args = parser.parse_args()
    
    setup_logging()
    
    thread = threading.Thread(target=worker, args=(args.domain, args.tlds, args.compounds, args.resolver))
    thread.start()
    thread.join()
    
if __name__ == "__main__":
    main()

