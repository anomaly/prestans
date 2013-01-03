## @package prestans.tools.templates.cocoah Cocoa header file template for preplate utility
#

extension = "h"

template = """#import <Foundation/Foundation.h>
#import "PTDefinitions.h"

%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
%if is_model or is_array:
@class ${namespace}${model};
%endif
%endfor

@interface ${namespace}${name} : NSObject <PTResponseParser>

%for ud, cc, ccif, is_model, is_array, model, required, min_length, max_length, minimum, maximum, choices, format, default in attributes:
%if model == "String":
@property (strong, nonatomic) NSString *${ccif};
%elif model == "Integer":
@property (assign) NSInteger ${ccif};
%elif model == "Float":
@property (assign) float ${ccif};
%elif model == "Boolean":
@property (assign) BOOL ${ccif};
%elif model == "DateTime":
@property (strong, nonatomic) NSDate *${ccif};
%elif is_model:
@property (strong, nonatomic) ${namespace}${model} *${ccif};
%elif is_array:
@property (strong, nonatomic) NSMutableArray *${ccif};
%endif
%endfor

@end
"""