from antlr4 import *
from IDLLexer import IDLLexer
from IDLParser import IDLParser
from IDLListener import IDLListener

class IDLToJSONListener(IDLListener):
    
    def __init__(self):
        self.json_schema = {}
        self.current_struct = None

    def enterStructDecl(self, ctx):
        print(f"Entering struct decl: {ctx.getText()}")
        # The parse tree shows the identifier is in ctx.identifier() not ctx.ID()
        if ctx.identifier():
            self.current_struct = ctx.identifier().getText()
        else:
            # Fallback if the grammar uses different naming
            for child in ctx.getChildren():
                if hasattr(child, 'getText'):
                    text = child.getText()
                    if text not in ['struct', '{', '}']:
                        self.current_struct = text
                        break
        
        if self.current_struct:
            self.json_schema[self.current_struct] = {
                "type": "object",
                "properties": {}
            }

    def enterMemberDecl(self, ctx):
        print(f"Entering member decl: {ctx.getText()}")
        if not self.current_struct:
            return
            
        # Get member name
        declarator = None
        if ctx.declarator():
            declarator = ctx.declarator()
        elif ctx.declarators() and ctx.declarators().declarator():
            declarator = ctx.declarators().declarator()
        
        if not declarator:
            return
            
        member_name = declarator.getText()
        
        # Handle type specification
        type_spec = ctx.type_spec()
        member_type = self._get_type_name(type_spec)

        type_map = {
            "float": "number",
            "double": "number",
            "boolean": "boolean",
            "short": "integer",
            "long": "integer",
            "string": "string",
            "octet": "integer"
        }
        
        self.json_schema[self.current_struct]["properties"][member_name] = {
            "type": type_map.get(member_type, member_type)
        }

    def _get_type_name(self, type_ctx):
        if type_ctx.simple_type_spec():
            base_type = type_ctx.simple_type_spec()
            if base_type.base_type_spec():
                return base_type.base_type_spec().getText()
            elif base_type.template_type_spec():
                return base_type.template_type_spec().getText()
            elif base_type.scoped_name():
                return base_type.scoped_name().getText()
        return type_ctx.getText()
    
class DebugListener(IDLListener):
    def enterEveryRule(self, ctx):
        print(f"Entered: {type(ctx).__name__}")
    
    def exitEveryRule(self, ctx):
        print(f"Exited: {type(ctx).__name__}")

def main():
    input_stream = FileStream("idl/example.idl")
    lexer = IDLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = IDLParser(stream)
    tree = parser.specification()
    
    
    # Debug: Print the parse tree
    from antlr4.tree.Trees import Trees
    print(Trees.toStringTree(tree, None, parser))
    
    listener = IDLToJSONListener()
    walker = ParseTreeWalker()
    
    walker.walk(DebugListener(), tree)
    walker.walk(listener, tree)
    
    import json
    print(json.dumps(listener.json_schema, indent=2))

if __name__ == "__main__":
    main()