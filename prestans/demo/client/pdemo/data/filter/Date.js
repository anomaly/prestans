/*
 * Automatically generated by preplate
 */

goog.provide('pdemo.data.filter.Date');

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
pdemo.data.filter.Date = function(opt_defaultValue) {

    if(opt_defaultValue != false)
        opt_defaultValue = true;

    this.dateRequired_ = opt_defaultValue;
    this.dateDefaultToday_ = opt_defaultValue;
    this.dateNotRequired_ = opt_defaultValue;
    this.dateDefaultString_ = opt_defaultValue;
};
goog.inherits(pdemo.data.filter.Date, prestans.types.Filter);



pdemo.data.filter.Date.prototype.dateRequired_ = null;
pdemo.data.filter.Date.prototype.dateDefaultToday_ = null;
pdemo.data.filter.Date.prototype.dateNotRequired_ = null;
pdemo.data.filter.Date.prototype.dateDefaultString_ = null;



pdemo.data.filter.Date.prototype.enableDateRequired = function() {
	this.dateRequired_ = true;
};
pdemo.data.filter.Date.prototype.enableDateDefaultToday = function() {
	this.dateDefaultToday_ = true;
};
pdemo.data.filter.Date.prototype.enableDateNotRequired = function() {
	this.dateNotRequired_ = true;
};
pdemo.data.filter.Date.prototype.enableDateDefaultString = function() {
	this.dateDefaultString_ = true;
};



pdemo.data.filter.Date.prototype.disableDateRequired = function() {
	this.dateRequired_ = false;
};
pdemo.data.filter.Date.prototype.disableDateDefaultToday = function() {
	this.dateDefaultToday_ = false;
};
pdemo.data.filter.Date.prototype.disableDateNotRequired = function() {
	this.dateNotRequired_ = false;
};
pdemo.data.filter.Date.prototype.disableDateDefaultString = function() {
	this.dateDefaultString_ = false;
};



pdemo.data.filter.Date.prototype.getDateRequired = function() {
    return this.dateRequired_;
};
pdemo.data.filter.Date.prototype.getDateDefaultToday = function() {
    return this.dateDefaultToday_;
};
pdemo.data.filter.Date.prototype.getDateNotRequired = function() {
    return this.dateNotRequired_;
};
pdemo.data.filter.Date.prototype.getDateDefaultString = function() {
    return this.dateDefaultString_;
};






pdemo.data.filter.Date.prototype.anyFieldsEnabled = function() {
    return (this.datetimeDefaultNow_ || this.datetimeDefaultString_ || this.datetimeNotRequired_ || this.datetimeRequired_ || this.timeDefaultNow_ || this.timeNotRequired_ || this.timeRequired_ || this.floatRequired_ || this.floatMinimum_ || this.floatNotRequired_ || this.floatMaximum_ || this.floatChoices_ || this.floatDefault_ || this.stringTitle_ || this.integerArray_.anyFieldsEnabled() || this.stringArray_.anyFieldsEnabled() || this.modelArray_.anyFieldsEnabled() || this.stringTitle_ || this.integerSample_.anyFieldsEnabled() || this.stringSample_.anyFieldsEnabled() || this.stringNotRequired_ || this.stringMaxLength_ || this.stringRequired_ || this.stringFormat_ || this.stringChoices_ || this.stringMinLength_ || this.stringDefault_ || this.dateRequired_ || this.dateDefaultToday_ || this.dateNotRequired_ || this.dateDefaultString_);
};



pdemo.data.filter.Date.prototype.getJSONObject = function(opt_complete) {

    if(opt_complete != true)
        opt_complete = false;

    var jsonifiedObject_ = {};
    
    if(this.dateRequired_ || opt_complete)
       jsonifiedObject_["date_required"] = this.dateRequired_;

    if(this.dateDefaultToday_ || opt_complete)
       jsonifiedObject_["date_default_today"] = this.dateDefaultToday_;

    if(this.dateNotRequired_ || opt_complete)
       jsonifiedObject_["date_not_required"] = this.dateNotRequired_;

    if(this.dateDefaultString_ || opt_complete)
       jsonifiedObject_["date_default_string"] = this.dateDefaultString_;


    return jsonifiedObject_;
};



pdemo.data.filter.Date.prototype.getJSONString = function(opt_complete) {

    if(opt_complete != true)
        opt_complete = false;

    return goog.json.serialize(this.getJSONObject(opt_complete));
};