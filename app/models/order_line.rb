class OrderLine < ApplicationRecord
  validates :id, uniqueness: true
end
