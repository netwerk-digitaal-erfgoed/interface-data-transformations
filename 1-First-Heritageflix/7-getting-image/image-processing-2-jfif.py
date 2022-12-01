from rdflib import Graph, URIRef
import os
import shutil
from timeit import default_timer as timer
from datetime import timedelta
import traceback
import urllib.request
import csv
import imageio.v2 as imageio
from PIL import ImageFile, Image
ImageFile.LOAD_TRUNCATED_IMAGES = True

start = timer()
print(start)

def startAPIProcessing(_path="./inputs/"):
    try:
        _entities = []
        for fName in os.listdir(_path):
            if not fName.endswith('.ttl'):
                continue
            _entities.append(fName.split(".")[0])
            startImageGathering(_entities)
    except Exception as e:
        print(str(e), traceback.format_exc())


def startImageGathering(_entities):
    try:
        for filename in _entities:
            result = f'./upload-pic/{filename}/'
            shutil.rmtree(result, ignore_errors=True)
            os.makedirs(result, exist_ok=True)
            path = f'./upload/{filename}.ttl'
            print(path)
            g = Graph()
            g.parse(path, format("ttl"))
            print(filename + " Parsed successfully")
            getByIdentifiers = """
            SELECT ?o ?ss
            WHERE {
                ?ss  ?p  ?s.
                ?s schema:contentUrl ?o .

            }"""
            qres = g.query(getByIdentifiers)
            for index, row in enumerate(qres):
                nameImgs= row.ss
                nameImg = nameImgs.split("/")[-1]
                try:
                    urllib.request.urlretrieve(row.o, f'{result}{nameImg}.jfif')
                    print(f'pictures saved on your computer, check {result}')

                except Exception as e:
                    print(str(e), traceback.format_exc(), f'check {filename} dataset : There is not object picture in subject {row.ss} and object {row.o} ')
                    result = './error-log/'
                    shutil.rmtree(result, ignore_errors=True)
                    os.makedirs(result, exist_ok=True)
                    with open(result + f'{filename}-error.csv', 'w', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f, quoting=csv.QUOTE_ALL, delimiter=',', quotechar='"')
                        f.write(",".join(["uri-records","uri-img"]))
                        f.write("\n")
                        for row in qres:
                            sub = row.ss.split("/n")[0]
                            obj = row.o.split("/n")[0]
                            writer.writerow([sub, obj])
                    print(f'{filename} saved in this path: {result}')

            # print("----------------------------------------------------------")

    except Exception as e:
      print(str(e), traceback.format_exc())

def startProcessingPictures(_path="."):
    try:

        for dirPath, dirNames, files in os.walk("."):
            _entities = []
            hasFile = False
            for fileName in [f for f in files if f.endswith(".jfif")]:
                hasFile = True
                _entities.append(fileName.split(".")[0])
            if hasFile:
                startEnrichment(_entities, dirPath)

    except Exception as e:
        print(str(e), traceback.format_exc())

def startEnrichment(_entities, _dirName):
    try:
        result = f'./report/'
        shutil.rmtree(result, ignore_errors=True)
        os.makedirs(result, exist_ok=True)

        gPathName = _dirName.replace(".\\","").replace("\\","//")
        dirName = gPathName.replace("//","-") ### for output file
        print("for final directory we should use it ", gPathName)
        folderInput = gPathName.split("//")[-1]
        resultFilePath = f'{result}/{dirName}-report.csv'
        with open(resultFilePath, 'a', encoding='utf-8', newline='') as csvResultValue:
            resultWriter = csv.writer(csvResultValue)
            resultWriter.writerow(["filename", "width", "height", "orientation"])

            for filename in _entities:
                print("here is dir",gPathName)
                print(f'{filename}.jfif')
                im = imageio.imread(f'./upload-pic/{folderInput}/{filename}.jfif') ###jfif
                # image.resize((h, w), Image.BICUBIC)
                width, height, channel = im.shape
                # print('width:  ', width, filename)
                # print('height: ', height, filename)
                if height > width:
                    orientation  = "Portrait"
                elif width > height:
                    orientation  = "landscape"
                elif height == width:
                    orientation = "square"
                print(orientation,filename)
                resultWriter = csv.writer(csvResultValue)
                resultWriter.writerow([filename, width, height, orientation])

    except Exception as e:
        print(str(e), traceback.format_exc())

# startAPIProcessing()
startProcessingPictures()
end = timer()
print(timedelta(seconds=end-start))