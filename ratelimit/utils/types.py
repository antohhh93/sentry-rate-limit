class Type:
    default = None
    expected_types = ()
    compatible_types = (str,)

    def __call__(self, value = None):
        if value is None:
            return self.default
        
        if isinstance(value, self.compatible_types):
            value = self.convert(value)

            if isinstance(value, self.expected_types):
                return value
            
            return self.default
    
    def convert(self, value):
        return value

class BoolType(Type):
    default = False
    expected_types = (bool,)
    compatible_types = (str, int)

    def convert(self, value):
        if isinstance(value, int):
            return bool(value)

        value = value.lower()
        
        if value in ("true", "1", "on"):
            return True
        
        if value in ("false", "0", "off"):
            return False

Bool = BoolType()
