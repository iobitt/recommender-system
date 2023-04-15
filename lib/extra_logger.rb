# frozen_string_literal: true

class ExtraLogger
  LOGGER = Rails.logger
  LEVELS = %i[error warn info].freeze

  LEVELS.each do |level|
    define_singleton_method level do |message, *args, **extra_params|
      tags = args.map { |tag| "[#{tag}]" }.join
      backtrace = message.respond_to?(:backtrace) ? message.backtrace&.first : ''
      message = "#{tags} #{message.to_s.squish} #{extra_params.presence} #{backtrace}"
      LOGGER.send(level, message)
    end
  end
end
