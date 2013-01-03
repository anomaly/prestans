## @package prestans.tools.templates.cocoah Cocoa header file template for preplate utility
#

extension = "m"

template = """#import "${namespace}${name}.h"
%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
%if is_model or is_array:
#import "${namespace}${model}.h"
%endif
%endfor

@implementation ${namespace}${name}

%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
@synthesize ${ccif} = __${ccif};
%endfor

-(id) init
{
    self = [super init];
    if (self)
    {
%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
%if is_array:
        self.${ccif} = [[NSMutableArray alloc] init];
%elif is_model:
%if required:
        self.${ccif} = [[${namespace}${model} alloc] init];
%else:
        self.${ccif} = nil;
%endif
%elif default == "NULL":
%if model == "String" or model == "DateTime":
        self.${ccif} = nil;
%endif
%else:
        self.${ccif} = ${default};
%endif
%endfor
    }
    return self;
}

- (id) initWithJSON:(id) jsonObject
{
    self = [super init];
    if (self)
    {
        NSDateFormatter *dateFormat = [[NSDateFormatter alloc] init];
        
%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
% if is_model:
%if required:
        self.${ccif} = [[${namespace}${model} alloc] init];
%else:
        if([jsonObject valueForKey:@"${ud}"] == NULL)
            self.${ccif} = nil;
        else
            self.${ccif} = [[${namespace}${model} alloc] initWithJSON:[jsonObject valueForKey:@"${ud}"]];
%endif
%elif is_array:
        self.${ccif} = [[NSMutableArray alloc] init];
        for (${namespace}${model} *object in [jsonObject valueForKey:@"${ud}"])
            [self.${ccif} addObject:object];
%elif model == "Integer":
        self.${ccif} = [[jsonObject objectForKey:@"${ud}"] integerValue];
%elif model == "Float":
        self.${ccif} = [[jsonObject objectForKey:@"${ud}"] floatValue];
%elif model == "String":
        self.${ccif} = [[jsonObject objectForKey:@"${ud}"] description];
%elif model == "Boolean":
        self.${ccif} = [[jsonObject objectForKey:@"${ud}"] boolValue];
%elif model == "DateTime":
        [dateFormat setDateFormat:@"YYYY-MM-dd hh:mm:ss"];
        self.${ccif} = [dateFormat dateFromString:[[jsonObject objectForKey:@"${format}"] description]];
%endif
%endfor

        dateFormat = nil;

    }
    return self;
}

@end
"""