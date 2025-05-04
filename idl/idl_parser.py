from antlr4 import *
from IDLLexer import IDLLexer
from IDLParser import IDLParser
from IDLListener import IDLListener

class IDLToJSONListener(IDLListener):
    def __init__(self):
        self.json_schema = {"definitions": {}}
        self.current_struct = None
        self.current_properties = None

    def enterStruct_type(self, ctx):
        # Get the struct name from identifier
        struct_name = ctx.identifier().getText()
        print(f"Found struct: {struct_name}")
        
        self.current_struct = struct_name
        self.current_properties = {}
        self.json_schema["definitions"][struct_name] = {
            "type": "object",
            "properties": self.current_properties
        }

    def enterMember(self, ctx):
        if not self.current_struct:
            return
            
        # Get type specification
        type_spec = ctx.type_spec()
        type_info = self._get_type_info(type_spec)
        
        # Get member names from declarators
        declarators = ctx.declarators()
        if declarators:
            for declarator in declarators.declarator():
                member_name = declarator.getText().rstrip(';')
                print(f"Found member: {member_name} of type {type_info}")
                self.current_properties[member_name] = type_info

    def _get_type_info(self, type_spec):
        type_map = {
            "float": {"type": "number", "format": "float"},
            "double": {"type": "number", "format": "double"},
            "boolean": {"type": "boolean"},
            "short": {"type": "integer", "format": "int16"},
            "long": {"type": "integer", "format": "int32"},
            "string": {"type": "string"},
            "octet": {"type": "integer", "format": "uint8"}
        }
        
        # Handle simple base types
        if type_spec.simple_type_spec():
            simple_type = type_spec.simple_type_spec()
            if simple_type.base_type_spec():
                base_type = simple_type.base_type_spec().getText()
                return type_map.get(base_type, {"type": base_type})
            elif simple_type.scoped_name():
                return {"$ref": f"#/definitions/{simple_type.scoped_name().getText()}"}
        
        # Handle sequences
        elif type_spec.template_type_spec():
            template = type_spec.template_type_spec()
            if template.getText().startswith('sequence'):
                inner_type = self._get_type_info(template.simple_type_spec())
                return {
                    "type": "array",
                    "items": inner_type,
                    "description": "sequence"
                }
        
        # Handle arrays (fixed size)
        elif type_spec.constr_type_spec():
            # This would handle array types if present
            pass
            
        return {"type": "unknown"}

def main():
    input_stream = FileStream("idl/example.idl")
    lexer = IDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = IDLParser(stream)
    
    print("=== RAW PARSE TREE ===")
    tree = parser.specification()
    from antlr4.tree.Trees import Trees
    print(Trees.toStringTree(tree, None, parser))
    
    print("\n=== WALKING TREE ===")
    listener = IDLToJSONListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    
    print("\n=== FINAL OUTPUT ===")
    import json
    print(json.dumps(listener.json_schema, indent=2))

if __name__ == "__main__":
    main()