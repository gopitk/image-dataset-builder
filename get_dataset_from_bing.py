from fastai2.vision.all import *

import argparse
from pathlib import Path
from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth

def search_images_bing(key, term, min_sz=128):
    client = api('https://api.cognitive.microsoft.com', auth(key))
    return L(client.images.search(query=term, count=100, min_height=min_sz, min_width=min_sz).value)

def stringToList(string):
    listRes = list(string.split(","))
    return listRes

def download_dataset(toplevelclass,subclasses,key):
    path = Path(toplevelclass)
    
    if not path.exists():
        path.mkdir()
        for o in subclasses:
            dest = (path/o)
            dest.mkdir(exist_ok=True)
            results = search_images_bing(key, f'{o} {toplevelclass}')
            download_images(dest, urls=results.attrgot('content_url'))
    
    fns = get_image_files(path)
    failed = verify_images(fns)
    failed.map(Path.unlink)
    print(f"Number of items in search: {len(fns)}. Number of Failed downloads: {len(failed)}. Number of downloaded images: {len(fns)-len(failed)}")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download bunch of images from Bing Image Search.')
	parser.add_argument('--classifier', help='Top level class of image objects you want')
	parser.add_argument('--subclasses', help='Comma separated list of subclasses of images to search')
	parser.add_argument('--key', help='Azure Bing Search API key')
	args = parser.parse_args()
	download_dataset(toplevelclass=args.classifier, subclasses=stringToList(args.subclasses), key=args.key)
