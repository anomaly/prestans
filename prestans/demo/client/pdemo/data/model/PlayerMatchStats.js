/*
 * Automatically generated by preplate
 */
goog.provide('pdemo.data.model.PlayerMatchStats');

goog.require('goog.json');

goog.require('prestans.types.Model.EventType');
goog.require('prestans.types.Model.AttributeChangedEvent');

goog.require('prestans.types.Model');

goog.require('prestans.types.Integer');

/**
 * @constructor
 * @extends {prestans.types.Model}
*/
pdemo.data.model.PlayerMatchStats = function(opt_json) {

    //Setup base model
    prestans.types.Model.call(this);

    if(goog.isDefAndNotNull(opt_json)) {
        this.matchId_ = new prestans.types.Integer({value: opt_json["match_id"], required: true, default: null, maximum: null, minimum: null, choices: null});
        this.tpa_ = new prestans.types.Integer({value: opt_json["tpa"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.ast_ = new prestans.types.Integer({value: opt_json["ast"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.stl_ = new prestans.types.Integer({value: opt_json["stl"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.minutes_ = new prestans.types.Integer({value: opt_json["minutes"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.tpm_ = new prestans.types.Integer({value: opt_json["tpm"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.reb_ = new prestans.types.Integer({value: opt_json["reb"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.pts_ = new prestans.types.Integer({value: opt_json["pts"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fta_ = new prestans.types.Integer({value: opt_json["fta"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fgm_ = new prestans.types.Integer({value: opt_json["fgm"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.pf_ = new prestans.types.Integer({value: opt_json["pf"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.blk_ = new prestans.types.Integer({value: opt_json["blk"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.playerId_ = new prestans.types.Integer({value: opt_json["player_id"], required: true, default: null, maximum: null, minimum: null, choices: null});
        this.ftm_ = new prestans.types.Integer({value: opt_json["ftm"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fga_ = new prestans.types.Integer({value: opt_json["fga"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.to_ = new prestans.types.Integer({value: opt_json["to"], required: true, default: 0, maximum: null, minimum: 0, choices: null});
    }
    else {
        this.matchId_ = new prestans.types.Integer({required: true, default: null, maximum: null, minimum: null, choices: null});
        this.tpa_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.ast_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.stl_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.minutes_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.tpm_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.reb_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.pts_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fta_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fgm_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.pf_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.blk_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.playerId_ = new prestans.types.Integer({required: true, default: null, maximum: null, minimum: null, choices: null});
        this.ftm_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.fga_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
        this.to_ = new prestans.types.Integer({required: true, default: 0, maximum: null, minimum: 0, choices: null});
    }
};
goog.inherits(pdemo.data.model.PlayerMatchStats, prestans.types.Model);



pdemo.data.model.PlayerMatchStats.prototype.matchId_ = null;
pdemo.data.model.PlayerMatchStats.prototype.tpa_ = null;
pdemo.data.model.PlayerMatchStats.prototype.ast_ = null;
pdemo.data.model.PlayerMatchStats.prototype.stl_ = null;
pdemo.data.model.PlayerMatchStats.prototype.minutes_ = null;
pdemo.data.model.PlayerMatchStats.prototype.tpm_ = null;
pdemo.data.model.PlayerMatchStats.prototype.reb_ = null;
pdemo.data.model.PlayerMatchStats.prototype.pts_ = null;
pdemo.data.model.PlayerMatchStats.prototype.fta_ = null;
pdemo.data.model.PlayerMatchStats.prototype.fgm_ = null;
pdemo.data.model.PlayerMatchStats.prototype.pf_ = null;
pdemo.data.model.PlayerMatchStats.prototype.blk_ = null;
pdemo.data.model.PlayerMatchStats.prototype.playerId_ = null;
pdemo.data.model.PlayerMatchStats.prototype.ftm_ = null;
pdemo.data.model.PlayerMatchStats.prototype.fga_ = null;
pdemo.data.model.PlayerMatchStats.prototype.to_ = null;


pdemo.data.model.PlayerMatchStats.prototype.getMatchId = function() {
    return this.matchId_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setMatchId = function(value) {
    var previousValue_ = this.matchId_.getValue();
    var success_ = this.matchId_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "matchId", previousValue_, this.matchId_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getTpa = function() {
    return this.tpa_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setTpa = function(value) {
    var previousValue_ = this.tpa_.getValue();
    var success_ = this.tpa_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "tpa", previousValue_, this.tpa_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getAst = function() {
    return this.ast_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setAst = function(value) {
    var previousValue_ = this.ast_.getValue();
    var success_ = this.ast_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "ast", previousValue_, this.ast_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getStl = function() {
    return this.stl_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setStl = function(value) {
    var previousValue_ = this.stl_.getValue();
    var success_ = this.stl_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "stl", previousValue_, this.stl_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getMinutes = function() {
    return this.minutes_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setMinutes = function(value) {
    var previousValue_ = this.minutes_.getValue();
    var success_ = this.minutes_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "minutes", previousValue_, this.minutes_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getTpm = function() {
    return this.tpm_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setTpm = function(value) {
    var previousValue_ = this.tpm_.getValue();
    var success_ = this.tpm_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "tpm", previousValue_, this.tpm_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getReb = function() {
    return this.reb_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setReb = function(value) {
    var previousValue_ = this.reb_.getValue();
    var success_ = this.reb_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "reb", previousValue_, this.reb_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getPts = function() {
    return this.pts_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setPts = function(value) {
    var previousValue_ = this.pts_.getValue();
    var success_ = this.pts_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "pts", previousValue_, this.pts_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getFta = function() {
    return this.fta_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setFta = function(value) {
    var previousValue_ = this.fta_.getValue();
    var success_ = this.fta_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "fta", previousValue_, this.fta_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getFgm = function() {
    return this.fgm_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setFgm = function(value) {
    var previousValue_ = this.fgm_.getValue();
    var success_ = this.fgm_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "fgm", previousValue_, this.fgm_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getPf = function() {
    return this.pf_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setPf = function(value) {
    var previousValue_ = this.pf_.getValue();
    var success_ = this.pf_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "pf", previousValue_, this.pf_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getBlk = function() {
    return this.blk_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setBlk = function(value) {
    var previousValue_ = this.blk_.getValue();
    var success_ = this.blk_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "blk", previousValue_, this.blk_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getPlayerId = function() {
    return this.playerId_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setPlayerId = function(value) {
    var previousValue_ = this.playerId_.getValue();
    var success_ = this.playerId_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "playerId", previousValue_, this.playerId_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getFtm = function() {
    return this.ftm_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setFtm = function(value) {
    var previousValue_ = this.ftm_.getValue();
    var success_ = this.ftm_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "ftm", previousValue_, this.ftm_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getFga = function() {
    return this.fga_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setFga = function(value) {
    var previousValue_ = this.fga_.getValue();
    var success_ = this.fga_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "fga", previousValue_, this.fga_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.getTo = function() {
    return this.to_.getValue();
};

pdemo.data.model.PlayerMatchStats.prototype.setTo = function(value) {
    var previousValue_ = this.to_.getValue();
    var success_ = this.to_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.AttributeChangedEvent(prestans.types.Model.EventType.ATTRIBUTE_CHANGED, "to", previousValue_, this.to_.getValue()));
    return success_;
};



pdemo.data.model.PlayerMatchStats.prototype.setValueForKey = function(key, value) {

    var returnVal_ = null;

    switch(key)
    {
        case "matchId":
            returnVal_ = this.setMatchId(value);
            break;
        case "tpa":
            returnVal_ = this.setTpa(value);
            break;
        case "ast":
            returnVal_ = this.setAst(value);
            break;
        case "stl":
            returnVal_ = this.setStl(value);
            break;
        case "minutes":
            returnVal_ = this.setMinutes(value);
            break;
        case "tpm":
            returnVal_ = this.setTpm(value);
            break;
        case "reb":
            returnVal_ = this.setReb(value);
            break;
        case "pts":
            returnVal_ = this.setPts(value);
            break;
        case "fta":
            returnVal_ = this.setFta(value);
            break;
        case "fgm":
            returnVal_ = this.setFgm(value);
            break;
        case "pf":
            returnVal_ = this.setPf(value);
            break;
        case "blk":
            returnVal_ = this.setBlk(value);
            break;
        case "playerId":
            returnVal_ = this.setPlayerId(value);
            break;
        case "ftm":
            returnVal_ = this.setFtm(value);
            break;
        case "fga":
            returnVal_ = this.setFga(value);
            break;
        case "to":
            returnVal_ = this.setTo(value);
            break;
        default:
            throw "Key: "+key+" not found in model";
    }

    return returnVal_;

};



pdemo.data.model.PlayerMatchStats.prototype.getJSONObject = function(opt_filter) {

    var jsonifiedObject_ = {};
    
    if(goog.isDef(opt_filter) && opt_filter.getMatchId())
        jsonifiedObject_["match_id"] = this.getMatchId()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["match_id"] = this.getMatchId()
    if(goog.isDef(opt_filter) && opt_filter.getTpa())
        jsonifiedObject_["tpa"] = this.getTpa()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["tpa"] = this.getTpa()
    if(goog.isDef(opt_filter) && opt_filter.getAst())
        jsonifiedObject_["ast"] = this.getAst()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["ast"] = this.getAst()
    if(goog.isDef(opt_filter) && opt_filter.getStl())
        jsonifiedObject_["stl"] = this.getStl()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["stl"] = this.getStl()
    if(goog.isDef(opt_filter) && opt_filter.getMinutes())
        jsonifiedObject_["minutes"] = this.getMinutes()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["minutes"] = this.getMinutes()
    if(goog.isDef(opt_filter) && opt_filter.getTpm())
        jsonifiedObject_["tpm"] = this.getTpm()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["tpm"] = this.getTpm()
    if(goog.isDef(opt_filter) && opt_filter.getReb())
        jsonifiedObject_["reb"] = this.getReb()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["reb"] = this.getReb()
    if(goog.isDef(opt_filter) && opt_filter.getPts())
        jsonifiedObject_["pts"] = this.getPts()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["pts"] = this.getPts()
    if(goog.isDef(opt_filter) && opt_filter.getFta())
        jsonifiedObject_["fta"] = this.getFta()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["fta"] = this.getFta()
    if(goog.isDef(opt_filter) && opt_filter.getFgm())
        jsonifiedObject_["fgm"] = this.getFgm()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["fgm"] = this.getFgm()
    if(goog.isDef(opt_filter) && opt_filter.getPf())
        jsonifiedObject_["pf"] = this.getPf()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["pf"] = this.getPf()
    if(goog.isDef(opt_filter) && opt_filter.getBlk())
        jsonifiedObject_["blk"] = this.getBlk()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["blk"] = this.getBlk()
    if(goog.isDef(opt_filter) && opt_filter.getPlayerId())
        jsonifiedObject_["player_id"] = this.getPlayerId()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["player_id"] = this.getPlayerId()
    if(goog.isDef(opt_filter) && opt_filter.getFtm())
        jsonifiedObject_["ftm"] = this.getFtm()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["ftm"] = this.getFtm()
    if(goog.isDef(opt_filter) && opt_filter.getFga())
        jsonifiedObject_["fga"] = this.getFga()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["fga"] = this.getFga()
    if(goog.isDef(opt_filter) && opt_filter.getTo())
        jsonifiedObject_["to"] = this.getTo()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["to"] = this.getTo()

    return jsonifiedObject_;
};

pdemo.data.model.PlayerMatchStats.prototype.getJSONString = function(opt_filter) {
    return goog.json.serialize(this.getJSONObject(opt_filter));
};