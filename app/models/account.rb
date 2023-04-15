# frozen_string_literal: true

class Account < ApplicationRecord
  has_many :categories
  has_many :products
  has_many :variants
  has_many :orders
  has_many :order_lines
end
