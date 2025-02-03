import base64
import zlib
import lzma
import time
import sys
from typing import List, Tuple


def base122_encode(rawData, warnings=True):
    if not isinstance(rawData, str):
        raise TypeError("rawData must be a string!")
    
    rawData = bytearray(rawData, "UTF-8")
    outData = bytearray()
    
    kIllegals = [0, 10, 13, 34, 38, 92]  # null, newline, carriage return, quote, ampersand, backslash
    kIllegalsSet = set(kIllegals)
    kShortened = 7  # Placeholder for shortened encoding strategy
    
    def extract_bits(data, start_index, bit_offset):
        """Efficiently extract 7 bits across byte boundaries."""
        byte1 = data[start_index]
        if bit_offset == 0:
            return byte1 & 0b01111111
        
        # Handle bit extraction across two bytes
        remainder_bits = 8 - bit_offset
        part1 = (byte1 << bit_offset) & 0b01111111
        if start_index + 1 < len(data):
            part2 = data[start_index + 1] >> remainder_bits
            return part1 | part2
        return part1

    curIndex = curBit = 0
    while curIndex < len(rawData):
        bits = extract_bits(rawData, curIndex, curBit)
        
        if bits not in kIllegalsSet:
            outData.append(bits)
            curBit += 7
            curIndex += curBit // 8
            curBit %= 8
            continue
        
        # Handle illegal characters
        illegalIndex = kIllegals.index(bits)
        
        # Attempt to get next 7-bit segment
        nextIndex = curIndex + (curBit + 7) // 8
        nextBits = extract_bits(rawData, nextIndex, (curBit + 7) % 8) if nextIndex < len(rawData) else bits
        
        # Encode illegal character
        b1 = 0b11000010
        b2 = 0b10000000
        
        if nextIndex >= len(rawData):
            b1 |= (0b111 & kShortened) << 2
            nextBits = bits
        else:
            b1 |= (0b111 & illegalIndex) << 2
        
        b1 |= 1 if (nextBits & 0b01000000) > 0 else 0
        b2 |= nextBits & 0b00111111
        
        outData.extend([b1, b2])
        
        # Update indices
        curBit += 14
        curIndex += curBit // 8
        curBit %= 8

    return outData


def compress_methods(urls: List[str]) -> List[Tuple[str, float, int]]:
    """
    Test compression methods for a list of URLs.
    
    Returns list of tuples: (method, compression time, compressed size)
    """
    results = []
    
    for method_name, compress_func in [
        ('base64+zlib', lambda x: zlib.compress(base64.b64encode(x.encode()))),
        ('base64+lzma', lambda x: lzma.compress(base64.b64encode(x.encode()))),
        ('base85+zlib', lambda x: zlib.compress(base64.b85encode(x.encode()))),
        ('base85', lambda x: base64.b85encode(x.encode())),
        ('base122', lambda x: base122_encode(x)),
        ('zlib', lambda x: zlib.compress(x.encode())),
        ('lzma', lambda x: lzma.compress(x.encode())),
        ('base122+zlib', lambda x: zlib.compress(base122_encode(x))),
        ('base122x2+zlib', lambda x: base122_encode(x)+base122_encode(x)),
        ('base122+lzma', lambda x: lzma.compress(base122_encode(x)))
    ]:
        total_time = 0
        total_size = 0
        
        for url in urls:
            start = time.time()
            try:
                compressed = compress_func(url)
                end = time.time()
                
                total_time += (end - start)
                total_size += len(compressed)
            except Exception as e:
                print(f"Error with {method_name}: {e}")
                break
        
        results.append((
            method_name, 
            total_time / len(urls), 
            total_size // len(urls)
        ))
    
    return results

def main():
    # Sample URL list - replace with your actual URLs
    urls = [
        'https://www.example.com/very/long/url/with/many/segments',
        'https://another.example.org/path/to/resource?param1=value1&param2=value2',
        'https://complex.url.net/search?q=test+query&category=all&sort=relevance',
        'https://www.example.com/',
        'https://www.example.com/login',
        'https://www.example.com/profile?user=alice#overview',
        'https://api.example.org/v1/users?id=42',
        'https://api.example.org/v1/users?id=43&sort=desc#section-1',
        'https://docs.example.net/guide/install?os=windows',
        'https://docs.example.net/guide/install?os=linux&step=2',
        'https://sub1.example.co/products/item-99?ref=summer_sale',
        'https://sub1.example.co/products/item-100?ref=summer_sale&utm_medium=email#promo',
        'https://sub2.example.com/categories/books?genre=fiction&sort=popularity',
        'https://sub2.example.com/categories/books?genre=nonfiction&sort=popularity#reviews',
        'https://www.example.org/search?q=unit+test',
        'https://www.example.org/search?q=encode+url#results',
        'https://www.example.net/account/settings?theme=dark',
        'https://www.example.net/account/settings?theme=light#display',
        'https://portal.example.co/dashboard?view=analytics',
        'https://portal.example.co/dashboard?view=analytics&year=2025',
        'https://shop.example.com/items/widget-A?color=red&size=large#tech-specs',
        'https://shop.example.com/items/widget-B?color=blue&size=small',
        'https://app.example.org/users/alice/feed?filter=unread',
        'https://app.example.org/users/bob/feed?filter=popular#timeline',
        'https://blog.example.net/2025/01/26/new-feature?highlight=true',
        'https://blog.example.net/2025/02/10/another-feature#comments',
        'https://www.example.co/api/data?offset=0&limit=25',
        'https://www.example.co/api/data?offset=25&limit=25',
        'https://files.example.com/download/report-2025.pdf',
        'https://files.example.com/download/report-2025.pdf?archive=true#part-2',
        'https://cdn.example.org/assets/main.css?v=1.2.3',
        'https://cdn.example.org/assets/main.css?v=1.2.4#hash-abc',
        'https://sub.example.net/x/y/z?abc=123',
        'https://sub.example.net/x/y/z?abc=456&xyz=789#footer',
        'https://www.example.com/checkout/shipping?method=express',
        'https://www.example.com/checkout/payment?coupon=SUMMER#billing',
        'https://www.example.org/downloads/release?version=beta',
        'https://www.example.org/downloads/release?version=stable#changelog',
        'https://update.example.net/autoupdate?channel=dev',
        'https://update.example.net/autoupdate?channel=stable#done',
        'https://docs2.example.co/how-to/encode-url?format=html',
        'https://docs2.example.co/how-to/encode-url?format=json#examples',
        'https://live.example.com/event/launch?ticket=VIP&ref=calendar#schedule',
        'javascript:alert(\'Hello, world!\')',
        'javascript:window.location=\'https://example.com\'',
        'javascript:alert(encodeURIComponent(\'URL Test\'));',
        'javascript:/*No operation*/;',
        'ftp://example.com/',
        'ftp://user:pass@example.com/',
        'ftp://example.org/pub/files/',
        'ftp://ftp.example.net/downloads/file.txt',
        'ftp://anonymous@example.co/uploads/data.csv',
        'ftp://demo:demo@ftp.example.io/public/',
        'ftp://example.org/pub/photos/image.jpg?type=raw',
        'ftp://user@example.com:2121/secret?ssl=true',
        'ftp://example.com/logs/2025-01-01.log',
        'ftp://user:PaSsW0rd!@files.example.com:21/backup.tar.gz',
        'ftp://example.org/path/to/something?option=1',
        'ftp://example.net/path?search=abc%20def',
        'ftp://sub.example.org/some/long/path/name?download=true',
        'http://www.example.com/',
        'http://www.example.org/index.html',
        'http://subdomain.example.net/page?param=test',
        'http://example.com/users/profile?id=123',
        'http://www.example.co/about#team',
        'http://blog.example.com/2025/01/26/article',
        'http://example.org/?q=unit+test#results',
        'http://example.net/shop/item?product=abc123&ref=promo',
        'http://example.net/login?returnTo=%2Fdashboard',
        'http://files.example.org/download?file=report.pdf',
        'http://example.org/api/data?offset=10&limit=5',
        'http://app.example.io/path/to/resource?user=alice',
        'http://www.example.com/with%20spaces?x=1',
        'https://www.example.com/',
        'https://secure.example.org/login',
        'https://docs.example.net/guide?os=linux#install',
        'https://portal.example.com/dashboard?view=stats',
        'https://shop.example.net/checkout?cart_id=xyz789',
        'https://example.org/secure?token=a1b2c3',
        'https://api.example.io/v1/users?id=42',
        'https://www.example.co/products/item-12?ref=campaignD',
        'https://sub.example.com/path?abc=123#section2',
        'https://www.example.com/search?q=test+data',
        'https://forum.example.net/topic/123?page=2',
        'https://cdn.example.org/assets/styles.css?v=2.0#minified'
    ]
    
    print("Compression Performance Test Results:")
    print("-" * 50)
    
    try:
        results = compress_methods(urls)
        
        print(f"{'Method':<15} {'Avg Time (s)':<15} {'Avg Size (bytes)':<20}")
        print("-" * 50)
        
        for method, avg_time, avg_size in results:
            print(f"{method:<15} {avg_time:<15.6f} {avg_size:<20}")
    
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == '__main__':
    main()