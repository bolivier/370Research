var fs = require('fs');
var mongodb = require('mongodb');
var assert = require('assert');

var Server = mongodb.Server;
var Db = mongodb.Db;

var db = new Db('research', new Server('localhost', 27017));
var counter = 0;

db.open(function (err, db) {

  // output: one json obj per line {text: <foo>, zipcode: <foobar>, userId: <poop>}

  fs.readFile(process.argv[2], function (err, data) {
    assert.equal(null, err);
    db.collection('zipcodes', function (err, collection) {
      assert.equal(null, err);
      JSON.parse(data).forEach(function (tweet) {
        collection.findOne({ geometry:
                      { $geoIntersects:
                        { $geometry :
                          { type: "Point",
                            coordinates: tweet.coordinates
                          }
                        }
                      }
                           },
        function (err, zipcodeRegion) {
          assert.equal(null, err);
          if (!zipcodeRegion) {
            return;
          }
          var zipcode = zipcodeRegion.properties.ZCTA5CE10;
					console.error('counter: ', counter);
					counter += 1;
          console.log(
            JSON.stringify(
              {
                text: tweet.text,
                userId: tweet.userId,
                zipcode: zipcode
              }
            )
          );
        });

        // if (zipcode !== undefined) {
        //   var result = {
        //     text: tweet.text,
        //     zipcode: zipcode.properties.ZCTA5CE10,
        //     userId: tweet.userId
        //   };
        //   console.log(JSON.stringify(result));
        // }
      });
    });
  });

});
