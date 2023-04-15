class AddUniqueIndexToAccountExternalId < ActiveRecord::Migration[7.0]
  def change
    add_index :accounts, :external_id, unique: true
  end
end
