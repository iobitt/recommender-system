require 'rainbow'
color_by_severite = {
  FATAL: :red,
  ERROR: :red,
  WARN: :yellow,
  INFO: :cyan,
  DEBUG: :magenta
}

logger = Logger.new(STDOUT)
formatter = Logger::Formatter.new
logger.formatter = proc do |severity, datetime, progname, msg|
  color = color_by_severite[severity.to_sym] || :white
  Rainbow(formatter.call(severity, datetime, progname, msg)).send(color)
end

Rails.logger = logger
ActiveRecord::Base.logger = logger
ActiveRecord.verbose_query_logs = true
Rails.logger.level = 0

require_relative '../../lib/extra_logger'
