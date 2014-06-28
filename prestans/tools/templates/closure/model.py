#!/usr/bin/env python
#
#  prestans, a standards based WSGI compliant REST framework for Python
#  http://prestans.googlecode.com
#
#  Copyright (c) 2013, Anomaly Software Pty Ltd.
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Anomaly Software nor the
#        names of its contributors may be used to endorse or promote products
#        derived from this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL Anomaly Software BE LIABLE FOR ANY
#  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

## @package prestans.tools.templates.closure.model Google Closure templates for preplate utility
#
# @todo Make array and DateTime only include if required
#

extension = "js"

template = """/*
 * Automatically generated by preplate
 */
<%!
    import prestans.tools.templates.closure.formatter as formatter
    from prestans.types import CONSTANT
%>
goog.provide('${namespace}.${name}');

goog.require('goog.json');

goog.require('prestans.types.Model.EventType');
goog.require('prestans.types.Model.ChangedEvent');

goog.require('prestans.types.Model');
<%

    dependencies = list()
    additional_args = list()
    for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
        if is_array and model == "String" or model == "Integer" or model == "Float" or model == "Boolean" or model == "DateTime" or model == "Date":
            full_path = "prestans.types."+model
        elif is_array and model == CONSTANT.ARRAY_DYNAMIC_ELEMENT_TEMPLATE:
            additional_args.append(ccif)
            full_path = None
        elif is_array:
            full_path = namespace+"."+model
        elif is_model:
            full_path = namespace+"."+model
        else:
            full_path = "prestans.types."+model

        if is_array and "prestans.types.Array" not in dependencies:
            dependencies.append("prestans.types.Array")

        if full_path is not None and full_path not in dependencies:
            dependencies.append(full_path)
%>
% for dependency in dependencies:
goog.require('${dependency}');
%endfor

/**
 * @constructor
 * @extends {prestans.types.Model}
*/
%if len(additional_args) > 0:
${namespace}.${name} = function(elementTemplates, opt_json) {
    if(goog.isDef(elementTemplates) && goog.isObject(elementTemplates))
        this.elementTemplates_ = elementTemplates;
    else
        throw "elementTemplates must be provided and of type object";
%else:
${namespace}.${name} = function(opt_json) {
%endif

    //Setup base model
    prestans.types.Model.call(this);

    if(goog.isDef(opt_json)) {
%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
    %if is_model:
        if(opt_json["${ud}"] == null)
            this.${ccif}_ = new ${namespace}.${model}();
        else
            this.${ccif}_ = new ${namespace}.${model}(opt_json["${ud}"]);
    %elif is_array:
        %if model == "String" or model == "Integer" or model == "Float" or model == "Boolean" or model == "DateTime" or model == "Date":
        this.${ccif}_ = new prestans.types.Array(prestans.types.${model}, null, opt_json["${ud}"], ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %elif model == CONSTANT.ARRAY_DYNAMIC_ELEMENT_TEMPLATE:
        this.${ccif}_ = new prestans.types.Array(this.elementTemplates_.${ccif}, null, opt_json["${ud}"], ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %else:
        this.${ccif}_ = new prestans.types.Array(${namespace}.${model}, null, opt_json["${ud}"], ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %endif
    %elif model == "String":
        this.${ccif}_ = new prestans.types.String(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.integer(max_length)}, ${formatter.integer(min_length)}, ${formatter.regexp(format)}, ${formatter.choices(choices)});
    %elif model == "Boolean":
        this.${ccif}_ = new prestans.types.Boolean(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.string(default)});
    %elif model == "Integer":
        this.${ccif}_ = new prestans.types.Integer(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.integer(maximum)}, ${formatter.integer(minimum)}, ${formatter.choices(choices)});
    %elif model == "Float":
        this.${ccif}_ = new prestans.types.Float(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.float(maximum)}, ${formatter.float(minimum)}, ${formatter.choices(choices)});
    %elif model == "DateTime":
        %if default == CONSTANT.DATETIME_NOW:
        this.${ccif}_ = new prestans.types.DateTime(opt_json["${ud}"], ${formatter.boolean(required)}, prestans.types.DateTime.NOW);
        %else:
        this.${ccif}_ = new prestans.types.DateTime(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.datetime(default)});
        %endif
    %elif model == "Date":
        %if default == CONSTANT.DATE_TODAY:
        this.${ccif}_ = new prestans.types.Date(opt_json["${ud}"], ${formatter.boolean(required)}, prestans.types.Date.TODAY);
        %else:
        this.${ccif}_ = new prestans.types.Date(opt_json["${ud}"], ${formatter.boolean(required)}, ${formatter.date(default)});
        %endif
    %endif
%endfor
    }
    else {
%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
    %if is_model: 
        this.${ccif}_ = new ${namespace}.${model}();
    %elif is_array:
        %if model == "String" or model == "Integer" or model == "Float" or model == "Boolean" or model == "DateTime" or model == "Date":
        this.${ccif}_ = new prestans.types.Array(prestans.types.${model}, null, null, ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %elif model == CONSTANT.ARRAY_DYNAMIC_ELEMENT_TEMPLATE:
        this.${ccif}_ = new prestans.types.Array(this.elementTemplates_.${ccif}, null, null, ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %else:
        this.${ccif}_ = new prestans.types.Array(${namespace}.${model}, null, null, ${formatter.integer(max_length)}, ${formatter.integer(min_length)});
        %endif
    %elif model == "String":
        this.${ccif}_ = new prestans.types.String(null, ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.integer(max_length)}, ${formatter.integer(min_length)}, ${formatter.regexp(format)}, ${formatter.choices(choices)});
    %elif model == "Boolean":
        this.${ccif}_ = new prestans.types.Boolean(null, ${formatter.boolean(required)}, ${formatter.string(default)});
    %elif model == "Integer":
        this.${ccif}_ = new prestans.types.Integer(null, ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.integer(maximum)}, ${formatter.integer(minimum)}, ${formatter.choices(choices)});
    %elif model == "Float":
        this.${ccif}_ = new prestans.types.Float(null, ${formatter.boolean(required)}, ${formatter.string(default)}, ${formatter.float(maximum)}, ${formatter.float(minimum)}, ${formatter.choices(choices)});
    %elif model == "DateTime":
        %if default == CONSTANT.DATETIME_NOW:
        this.${ccif}_ = new prestans.types.DateTime(null, ${formatter.boolean(required)}, prestans.types.DateTime.NOW);
        %else:
        this.${ccif}_ = new prestans.types.DateTime(null, ${formatter.boolean(required)}, ${formatter.datetime(default)});
        %endif
    %elif model == "Date":
        %if default == CONSTANT.DATE_TODAY:
        this.${ccif}_ = new prestans.types.Date(null, ${formatter.boolean(required)}, prestans.types.Date.TODAY);
        %else:
        this.${ccif}_ = new prestans.types.Date(null, ${formatter.boolean(required)}, ${formatter.date(default)});
        %endif
    %endif
%endfor
    }
};
goog.inherits(${namespace}.${name}, prestans.types.Model);

%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
${namespace}.${name}.prototype.${ccif}_ = null;
%if format:
${namespace}.${name}.${cc}StringFormat = new RegExp("${format}");
%endif
%if choices:
${namespace}.${name}.${cc}Choices = ${choices};
%endif
%endfor

%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
${namespace}.${name}.prototype.get${cc} = function() {
%if is_model or is_array:
    return this.${ccif}_;
%else:
    return this.${ccif}_.getValue();
%endif
};

${namespace}.${name}.prototype.set${cc} = function(value) {
%if is_array:
    var previousArray_ = this.${ccif}_;
    %if model == "Integer" or model == "String" or model == "Float" or model == "Boolean" or model == "DateTime" or model == "Date":
    if(value instanceof prestans.types.Array && value.getElementTemplate() == prestans.types.${model}) {
    %elif model == CONSTANT.ARRAY_DYNAMIC_ELEMENT_TEMPLATE:
    if(value instanceof prestans.types.Array && value.getElementTemplate() == this.elementTemplates_.${ccif}) {
    %else:
    if(value instanceof prestans.types.Array && value.getElementTemplate() == ${namespace}.${model}) {
    %endif
        this.${ccif}_ = value;
        this.dispatchEvent(new prestans.types.Model.ChangedEvent(prestans.types.Model.EventType.CHANGED, "${ccif}", previousArray_, this.${ccif}_));
        return true;
    }
    else
        return false;
%elif is_model:
    var previousModel_ = this.${ccif}_;
    if(value instanceof ${namespace}.${model}) {
        this.${ccif}_ = value;
        this.dispatchEvent(new prestans.types.Model.ChangedEvent(prestans.types.Model.EventType.CHANGED, "${ccif}", previousModel_, this.${ccif}_));
        return true;
    }
    else
        return false;
%else:
    var previousValue_ = this.${ccif}_.getValue();
    var success_ = this.${ccif}_.setValue(value);
    this.dispatchEvent(new prestans.types.Model.ChangedEvent(prestans.types.Model.EventType.CHANGED, "${ccif}", previousValue_, this.${ccif}_.getValue()));
    return success_;
%endif
};



%endfor

${namespace}.${name}.prototype.setValueForKey = function(key, value) {

    var returnVal_ = null;

    switch(key)
    {
% for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
        case "${ccif}":
            returnVal_ = this.set${cc}(value);
            break;
%endfor
        default:
            throw "Key: "+key+" not found in model";
    }

    return returnVal_;

};


${namespace}.${name}.prototype.getJSONObject = function(opt_filter) {

    var jsonifiedObject_ = {};
    
% for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
%if is_model:
    if(goog.isDef(opt_filter) && opt_filter.get${cc}().anyFieldsEnabled()) {
        if(this.get${cc}() == null)
            jsonifiedObject_["${ud}"] = null;
        else
            jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject(opt_filter.get${cc}());
    }
    else if(!goog.isDef(opt_filter)) {
        if(this.get${cc}() == null)
            jsonifiedObject_["${ud}"] = null;
        else
            jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject();
    }
%elif is_array:
    %if model == "Integer" or model == "String" or model == "Float" or model == "Boolean" or model == "DateTime" or model == "Date":
    if(goog.isDef(opt_filter) && opt_filter.get${cc}())
        jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject(opt_filter.get${cc}());
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject();
    %else:
    if(goog.isDef(opt_filter) && opt_filter.get${cc}().anyFieldsEnabled())
        jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject(opt_filter.get${cc}());
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["${ud}"] = this.get${cc}().getJSONObject();
    %endif
%elif model == "DateTime":
    if(goog.isDef(opt_filter) && opt_filter.get${cc}())
        jsonifiedObject_["${ud}"] = this.${ccif}_.getJSONObject();
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["${ud}"] = this.${ccif}_.getJSONObject();
%elif model == "Date":
    if(goog.isDef(opt_filter) && opt_filter.get${cc}())
        jsonifiedObject_["${ud}"] = this.${ccif}_.getJSONObject();
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["${ud}"] = this.${ccif}_.getJSONObject();
%else:
    if(goog.isDef(opt_filter) && opt_filter.get${cc}())
        jsonifiedObject_["${ud}"] = this.get${cc}()
    else if(!goog.isDef(opt_filter))
        jsonifiedObject_["${ud}"] = this.get${cc}()
%endif
%endfor

    return jsonifiedObject_;
};

${namespace}.${name}.prototype.getJSONString = function(opt_filter) {
    return goog.json.serialize(this.getJSONObject(opt_filter));
};

"""