/*
 * Automatically generated by preplate
 */

goog.provide('pdemo.data.filter.ModelSample');

goog.require('goog.json');
goog.require('goog.object');

goog.require('prestans.types.Filter');

goog.require('pdemo.data.filter.Integer');
goog.require('pdemo.data.filter.String');
goog.require('pdemo.data.filter.IntegerSample');
goog.require('pdemo.data.filter.StringSample');

/**
 * @constructor
*/
pdemo.data.filter.ModelSample = function(opt_defaultValue) {

    if(opt_defaultValue != false)
        opt_defaultValue = true;

    this.stringTitle_ = opt_defaultValue;
    this.integerSample_ = new pdemo.data.filter.IntegerSample(opt_defaultValue);
    this.stringSample_ = new pdemo.data.filter.StringSample(opt_defaultValue);
};
goog.inherits(pdemo.data.filter.ModelSample, prestans.types.Filter);



pdemo.data.filter.ModelSample.prototype.stringTitle_ = null;
pdemo.data.filter.ModelSample.prototype.integerSample_ = null;
pdemo.data.filter.ModelSample.prototype.stringSample_ = null;



pdemo.data.filter.ModelSample.prototype.enableStringTitle = function() {
	this.stringTitle_ = true;
};
pdemo.data.filter.ModelSample.prototype.enableIntegerSample = function() {
    this._ = new pdemo.data.filter.IntegerSample(true);
};
pdemo.data.filter.ModelSample.prototype.enableStringSample = function() {
    this._ = new pdemo.data.filter.StringSample(true);
};



pdemo.data.filter.ModelSample.prototype.disableStringTitle = function() {
	this.stringTitle_ = false;
};
pdemo.data.filter.ModelSample.prototype.disableIntegerSample = function() {
    this.integerSample_ = new pdemo.data.filter.IntegerSample(false);
};
pdemo.data.filter.ModelSample.prototype.disableStringSample = function() {
    this.stringSample_ = new pdemo.data.filter.StringSample(false);
};



pdemo.data.filter.ModelSample.prototype.getStringTitle = function() {
    return this.stringTitle_;
};
pdemo.data.filter.ModelSample.prototype.getIntegerSample = function() {
    return this.integerSample_;
};
pdemo.data.filter.ModelSample.prototype.getStringSample = function() {
    return this.stringSample_;
};



pdemo.data.filter.ModelSample.prototype.setIntegerSample = function(integerSample) {
    if(integerSample instanceof pdemo.data.filter.IntegerSample)
        this.integerSample_ = integerSample;
    else
        throw "integerSample must be of type pdemo.data.filter.IntegerSample";
};
pdemo.data.filter.ModelSample.prototype.setStringSample = function(stringSample) {
    if(stringSample instanceof pdemo.data.filter.StringSample)
        this.stringSample_ = stringSample;
    else
        throw "stringSample must be of type pdemo.data.filter.StringSample";
};



pdemo.data.filter.ModelSample.prototype.anyFieldsEnabled = function() {
    return (this.datetimeDefaultNow_ || this.datetimeDefaultString_ || this.datetimeNotRequired_ || this.datetimeRequired_ || this.timeDefaultNow_ || this.timeNotRequired_ || this.timeRequired_ || this.floatRequired_ || this.floatMinimum_ || this.floatNotRequired_ || this.floatMaximum_ || this.floatChoices_ || this.floatDefault_ || this.stringTitle_ || this.integerArray_.anyFieldsEnabled() || this.stringArray_.anyFieldsEnabled() || this.modelArray_.anyFieldsEnabled() || this.stringTitle_ || this.integerSample_.anyFieldsEnabled() || this.stringSample_.anyFieldsEnabled());
};



pdemo.data.filter.ModelSample.prototype.getJSONObject = function(opt_complete) {

    if(opt_complete != true)
        opt_complete = false;

    var jsonifiedObject_ = {};
    
    if(this.stringTitle_ || opt_complete)
       jsonifiedObject_["string_title"] = this.stringTitle_;

    if(this.integerSample_ != null && !goog.object.isEmpty(this.integerSample_.getJSONObject(opt_complete)))
        jsonifiedObject_["integer_sample"] = this.integerSample_.getJSONObject(opt_complete);
    else if(opt_complete)
        jsonifiedObject_["integer_sample"] = false;

    if(this.stringSample_ != null && !goog.object.isEmpty(this.stringSample_.getJSONObject(opt_complete)))
        jsonifiedObject_["string_sample"] = this.stringSample_.getJSONObject(opt_complete);
    else if(opt_complete)
        jsonifiedObject_["string_sample"] = false;


    return jsonifiedObject_;
};



pdemo.data.filter.ModelSample.prototype.getJSONString = function(opt_complete) {

    if(opt_complete != true)
        opt_complete = false;

    return goog.json.serialize(this.getJSONObject(opt_complete));
};