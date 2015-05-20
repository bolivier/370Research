# Twitter Research

2015 Research about happiness and Twitter with Dr. Philip Cannata by Nick Sundin and Brandon Olivier. 

## Getting the Tweets

We have a list of Twitter users in pieces (for faster gathering) in the training_subset[1234].txt files.  Those files need to be passed to `timelines_new.py`.  That file is called like this: `python3 timelines-new.py training_subset[1234].txt <account index>`.  That file does call `print` for showing progress, so python3 is required.

The result of that function is to create a file with the same name as the input file (training_subset[1234].txt in the above example) with ".results.txt" concatenated to the end.

### Flatten Tweets

The tweets even at this point have an unusual format, and need to be flattened.  We have a file called the_flattener.py and it's run with `python3 the_flattener.py grabbed.json > flattened.txt`.  Python 3 is required because it calls print as a function.  

## Associate Zip codes

To associate geolocation coordinates to a zip code, we have to grab shape files of the zip codes from the US government and then convert those into a geoJSON file then upload that into a MongoDB instance.  From that, it is trivial to create queries for Mongo to query whether abstracted locations in a shape.

### Get Shapefiles

We got a library of shapefiles from `https://github.com/mbostock/us-atlas` which is cloned with `git clone https://github.com/mbostock/us-atlas.git`.  Then cd into that directory, and run `make shp/us/zipcodes-unmerged.shp`.  That will download the full shape files from the US census website.

That file is too large.  To compress the file run `ogr2ogr simplify .001 simple.shp shp/us/zipcodes-unmerged.shp`.

Since MongoDB is written in Javascript, we need to convert that .shp file to a json file.  To convert to geoJSON `ogr2ogr -f GeoJSON zipcodes.json simple.shp`, where simple.shp is a file that was created in the last step. 

### Load Shapefiles into Mongo

To import the json file into mongo use: `mongoimport zipcodes.json --db research --collection zipcodes`.  Sometimes that doesn't work exactly right and we need to include the `--jsonArray` as a flag to get the representation working completely right.

### Query Mongo with Tweets

Mongo queries about zip codes take the form of
```
                    db.collection.findOne({ geometry:
                      { $geoIntersects:
                        { $geometry :
                          { type: "Point",
                            coordinates: tweet.coordinates
                          }
                        }
                      }}, callbackFunction);
```
#### UserFiler 

To associate each tweet with a zip code, run the file `userFiler.js`.  In line with unix practices, that command simply outputs the text that it returns (simplified json).  So that command would be run like `node userFiler.js tweets.txt > {{ filename for simplified tweets}}`.

## Aggregate with Spark

After installing Spark from the website and formatting the data with the required information, we can convert the individual tweets into aggregates.  The command to do that is `spark-submit twitter-aggregator.py tweeets_all.flattened.zip.txt > tweets_with_counts.aggregate.txt`

## Convert Aggregates into CSV

The txt file, so that it can be imported into databases, needs to be converted into a csv file.  The python code to do that is in output_converter.py.  That script doesn't output any text, so it should work with python 2 or 3.  We used 3.  It's run with `python output_converter.py tweets_with_counts.aggregate.txt aggregates.csv` which will produce a csv file. 
