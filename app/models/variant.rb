class Variant < ApplicationRecord
  validates :id, uniqueness: true
end
