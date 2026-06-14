.headers on
.mode column

SELECT 'COMMUNICATION LAYERS' AS section;
SELECT communication_layer, description, typical_failure
FROM communication_layer_type
ORDER BY communication_layer;

SELECT 'COMMUNICATION RECORDS REQUIRING REVIEW' AS section;
SELECT record_key, communication_layer, audience, message_goal
FROM communication_record
WHERE status IN ('review', 'revise');

SELECT 'UNCERTAINTY MESSAGES' AS section;
SELECT message_key, uncertainty_type, plain_language_statement, decision_relevance
FROM uncertainty_message
ORDER BY uncertainty_type;

SELECT 'AUDIENCE GUIDE' AS section;
SELECT audience, main_need, communication_emphasis
FROM audience_guide
ORDER BY audience;

SELECT 'DECISION AND GOVERNANCE COMMUNICATION TARGETS' AS section;
SELECT record_key, communication_layer, audience, plain_language_statement
FROM communication_record
WHERE communication_layer IN ('decision_threshold', 'model_limit', 'governance');
