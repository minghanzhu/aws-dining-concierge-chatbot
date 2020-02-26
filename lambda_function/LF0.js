var AWS = require("aws-sdk");
var lexruntime = new AWS.LexRuntime();
var BOT_NAME = "DiningConciergeChatBot";
var BOT_ALIAS = "Prod";
var ERROR_RESP = "Oh no, Something's gone wrong. Please try again later.";

exports.handler = (event, context, callback) => {
    var id = event.messages[0].unstructured.id;
    var message = event.messages[0].unstructured.text;

    var params = {
        botAlias: BOT_ALIAS,
        botName: BOT_NAME,
        inputText: message,
        userId: id,
        requestAttributes: {},
        sessionAttributes: {}
    };

    // Make the request and handle the response
    lexruntime.postText(params, function(err, data) {
        if (err) {
            console.log(err);
            callback(ERROR_RESP+": "+err);
        }
        else {
            callback(data.message);
        }
    });
};
