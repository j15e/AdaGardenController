variable "lambba_env" {
  type = "map"
}

resource "aws_lambda_function" "ada_garden_controller" {
  filename = "../AdaGardenController.zip"
  source_code_hash = "${base64sha256(file("../AdaGardenController.zip"))}"
  description =  "A job to check weather data and trigger or not watering."
  function_name = "ada_garden_controller"
  runtime = "python3.6"
  timeout = 60
  memory_size = 128
  role = "${aws_iam_role.iam_for_garden_controller_lambda.arn}"
  handler = "lambda_function.handler"
  environment {
    variables = "${var.lambba_env}"
  }
}

resource "aws_cloudwatch_event_rule" "every_morning" {
  name                = "every-morning"
  description         = "Fires every minute every morning between 3AM and 10AM."
  schedule_expression = "cron(* 3,4,5,6,7,8,9,10 ? * * *)"
}

resource "aws_cloudwatch_event_target" "check_watering_every_morning" {
  rule      = "${aws_cloudwatch_event_rule.every_morning.name}"
  target_id = "ada_garden_controller"
  arn       = "${aws_lambda_function.ada_garden_controller.arn}"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_ada_garden_controller" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = "${aws_lambda_function.ada_garden_controller.function_name}"
  principal     = "events.amazonaws.com"
  source_arn    = "${aws_cloudwatch_event_rule.every_morning.arn}"
}
