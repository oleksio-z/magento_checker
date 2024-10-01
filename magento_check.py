import asyncio
import aiohttp
import aiofiles
import argparse
import random
import re
from termcolor import colored

MAGENTO_SIGNS = 3

# Список User-Agent
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    # Add more User-Agents here
]

def main():
    usage = "Usage: python script.py [-ct] [--connection_attempts] [-lc] [--limit_of_calls] [-t] [--timeout] [-ms] [--magento_signs] input_filename output_filename"
    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("-ct", "--connection_attempts", default=3, type=int)
    parser.add_argument("-lc", "--limit_of_calls", default=50, type=int)
    parser.add_argument("-t", "--timeout", default=5, type=int)
    parser.add_argument("-ms", "--magento_signs", default=3, type=int)
    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    args = parser.parse_args()

    asyncio.run(process_files(args.input_filename, args.output_filename,
                args.limit_of_calls, args.timeout, args.magento_signs))


async def process_files(infilename, outfilename, limit, timeout, magento_signs):
    semaphore = asyncio.Semaphore(limit)
    counters = [0, 0]
    tasks = []

    async with aiofiles.open(outfilename, 'w') as outfile:
        async with aiofiles.open(infilename, 'r') as infile:
            async for domain in infile:
                domain = domain.strip()
                if domain:
                    async with semaphore:
                        tasks.append(asyncio.create_task(analyze_domain(domain, outfile, counters, timeout, magento_signs)))
                        tasks = list(filter(lambda t: t and not t.done(), tasks))
            await asyncio.gather(*tasks)


async def analyze_domain(url, outfile, counters, timeout, magento_signs):
    if url:
        check = await fetch_html(url, timeout, magento_signs)
        counters[1] += 1
        if check:
            counters[0] += 1
            print(colored(f"[OK] {url} | Found:{counters[0]}| Processed: {counters[1]}", "green"))
            await outfile.write(url + "\n")  # Add newline after URL
        else:
            print(colored(f"[ERR] {url} | Found:{counters[0]}| Processed: {counters[1]}", "red"))
            return


async def fetch_html(url, timeout, magento_signs):
    checks = [
        ('/index.php/admin/', 'login'),
        ('/RELEASE_NOTES.txt', 'magento'),
        ('/js/mage/cookies.js', ''),
        ('/index.php', '/mage/'),
        ('/skin/frontend/default/default/css/styles.css', ''),
        ('/errors/design.xml', 'magento')
    ]
    user_agent = random.choice(USER_AGENTS)
    headers = {'User-Agent': user_agent}
    counter = 0
    async with aiohttp.ClientSession(headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    magento_signatures_regex = [
                        r'X-Magento-Vary',
                        r'Magento_GoogleTagManager/js/google-tag-manager',
                        r'type\s*=\s*[\"\']text/x-magento-init[\"\']',
                        r'r\.cart_type\s*=\s*[\"\']MAGENTO[\"\']',
                        r'Magento_PageBuilder',
                        r'Magento_Theme',
                        r'data-mage-init',
                        r'\/js\/mage\/cookies\.js[\'\"]',
                        r'\/mage\.js[\'\"]',
                    ]
                    for signature in magento_signatures_regex:
                        if re.search(signature, html):
                            counter += 1

                for path, keyword in checks:
                    try:
                        async with session.get(url + path) as resp:
                            if resp.status == 200:
                                text = await resp.text()
                                if keyword in text and "404" not in text:
                                    counter += 1
                    except:
                        return None

        except:
            return None

    return counter > magento_signs


if __name__ == '__main__':
    main()
