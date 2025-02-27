from viktor._vendor import libcst

_OBJECTS = {
    "GeometryView",
    "GeometryAndDataView",
}


class Visitor(libcst.CSTVisitor):
    pass


class Transformer(libcst.CSTTransformer):

    def __init__(self, visitor):
        super().__init__()
        self.ImportALIAS = _OBJECTS

    def leave_ImportAlias_asname(self, node) -> None:
        if node.name.value in _OBJECTS:
            if node.asname:
                self.ImportALIAS.remove(node.name.value)
                self.ImportALIAS.add(node.asname.name.value)

    def leave_Call(self, node, updated_node):
        try:
            if node.func.value not in self.ImportALIAS:
                return updated_node
        except AttributeError:  # func may not have 'value'
            return updated_node

        is_2d = False
        up_axis_is_y = False
        x_axis_to_right_is_present = False

        for arg in node.args:
            if arg.keyword is not None:
                if arg.keyword.value == 'x_axis_to_right':
                    x_axis_to_right_is_present = True

                if arg.keyword.value == 'view_mode':
                    if arg.value.value == "'2D'":
                        is_2d = True

                if arg.keyword.value == 'up_axis':
                    if arg.value.value == "'Y'":
                        up_axis_is_y = True

        if not is_2d and not up_axis_is_y and not x_axis_to_right_is_present:
            new_args = list(node.args)
            new_args.append(
                libcst.Arg(
                    keyword=libcst.Name('x_axis_to_right'),
                    value=libcst.Name('False'),
                    equal=libcst.AssignEqual(
                        whitespace_before=libcst.SimpleWhitespace(''),
                        whitespace_after=libcst.SimpleWhitespace(''),
                    ),
                )
            )

            return updated_node.with_changes(args=new_args)

        return updated_node
