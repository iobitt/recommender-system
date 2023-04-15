# frozen_string_literal: true

class CreateCategoriesService < ApplicationService
  attr_accessor :account

  def initialize(account)
    @account = account
  end

  def call
    raise 'inSales API not configured!' unless InsalesApi::Category.init(account)

    InsalesApi::Category.all.each { account.categories.create(_1.attributes) }
  end
end
