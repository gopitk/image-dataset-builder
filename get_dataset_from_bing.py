from fastai2.vision.all import *

import argparse
from pathlib import Path
from azure.cognitiveservices.search.imagesearch import ImageSearchClient as api
from msrest.authentication import CognitiveServicesCredentials as auth

def search_images_bing(key, term, min_sz=128, numimages=100):
    client = api('https://api.cognitive.microsoft.com', auth(key))
    return L(client.images.search(query=term, count=numimages, min_height=min_sz, min_width=min_sz).value)

def stringToList(string):
    listRes = list(string.split(","))
    return listRes

def download_dataset(toplevelclass,subclasses,key,numimages,suffix):
    path = Path(toplevelclass)
    
    if not path.exists():
        path.mkdir()
        for o in subclasses:
            dest = (path/o)
            dest.mkdir(exist_ok=True)
            results = search_images_bing(key, f'{o} {suffix}', numimages=numimages)
            download_images(dest, urls=results.attrgot('content_url'))
    
    fns = get_image_files(path)
    failed = verify_images(fns)
    failed.map(Path.unlink)
    print(f"Number of items in search: {len(fns)}. Number of Failed downloads: {len(failed)}. Number of downloaded images: {len(fns)-len(failed)}")

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Download bunch of images from Bing Image Search.')
	parser.add_argument('--classifier', help='Top level class of image objects you want', required=True)
	parser.add_argument('--subclasses', help='Comma separated list of subclasses of images to fetch', required=True)
	parser.add_argument('--key', help='Azure Bing Search API key', required=True)
	parser.add_argument('--numimages', help='Number of images per class to fetch', type=int, default=50)
	parser.add_argument('--nosuffix', help='Optional flag to not suffix subsclass with top level class in image search', nargs='?',type=bool, const=True, default=False)
	args = parser.parse_args()
	suffix = '' if args.nosuffix else args.classifier
	download_dataset(toplevelclass=args.classifier, subclasses=stringToList(args.subclasses), key=args.key, numimages=args.numimages, suffix=suffix )
