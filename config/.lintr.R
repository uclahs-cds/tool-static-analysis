linters <- linters_with_defaults(
    defaults = list(),
    assignment_linter(),
    object_name_linter(regexes=c("dotted.Mixed.case"="^\\.?[A-Za-z0-9]+(\\.[A-Za-z0-9]+)*$")),
    bl_brace_linter = (function() {
        base_linter <- brace_linter()
        Linter(linter_level = "expression", function(source_file) {
            lints <- base_linter(source_file)
            Filter(function(lint) {
                lint$message == "[bl_brace_linter] `else` should come on the same line as the previous `}`."
            }, lints)
        })
    })(),
    function_left_parentheses_linter(),
    quotes_linter(delimiter = "'"),
    spaces_left_parentheses_linter(),
    trailing_blank_lines_linter(),
    trailing_whitespace_linter(),
    infix_spaces_linter(exclude_operators="~")
)

exclusions <- (function() {
    new_excludes <- list(".lintr.R")

    existing_excludes <- tryCatch(
        {
            if (file.exists("/tmp/lint/.lintr")) {
                default_settings <- lintr:::read_config_file("/tmp/lint/.lintr");

                if (exists("exclusions", default_settings)) {
                    default_settings$exclusions
                } else {
                    list()
                }
            }
        },
        error = function(e) {
            message("Error while trying to import .lintr: ", e$message)
            list()
        }
    )

    c(new_excludes, existing_excludes)
})()
