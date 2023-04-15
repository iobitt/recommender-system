# frozen_string_literal: true

class InsalesApi::Base < ActiveResource::Base
  @configured = false

  def self.init(account)
    self.site = "http://#{account.shop}/admin/"
    self.user = 'recommender-system'
    self.password = account.password
    @configured = true
  end

  def self.configured?
    !!@configured
  end
end
