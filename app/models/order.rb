class Order < ApplicationRecord
  validates :id, uniqueness: true
end
