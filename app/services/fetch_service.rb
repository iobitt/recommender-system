# frozen_string_literal: true

class FetchService < ApplicationService
  PER_PAGE = 100

  attr_accessor :account, :active_resource, :block

  def initialize(account, active_resource, &block)
    @account = account
    @active_resource = active_resource
    @block = block
  end

  def call
    page = 1
    last_id = nil
    loop do
      response = active_resource.all(params: { per_page: PER_PAGE, page: })
      return unless response

      # У категорий нет пагинации. Будет бесконечный цикл, если ничего не предпринять
      response_last_id = response.last&.attributes&.dig('id')
      return if last_id == response_last_id

      response.each { block.call(_1) }
      last_id = response_last_id
      page += 1
    end
  end
end
