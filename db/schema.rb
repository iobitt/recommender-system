# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2023_04_16_102647) do
  create_table "accounts", force: :cascade do |t|
    t.integer "external_id", null: false
    t.text "shop", null: false
    t.text "password", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["external_id"], name: "index_accounts_on_external_id", unique: true
  end

  create_table "categories", force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "parent_id"
    t.text "title", null: false
    t.integer "position", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["account_id"], name: "index_categories_on_account_id"
  end

  create_table "order_lines", force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "order_id", null: false
    t.integer "product_id", null: false
    t.integer "variant_id", null: false
    t.text "title", null: false
    t.integer "quantity", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["account_id"], name: "index_order_lines_on_account_id"
    t.index ["order_id"], name: "index_order_lines_on_order_id"
    t.index ["product_id"], name: "index_order_lines_on_product_id"
    t.index ["variant_id"], name: "index_order_lines_on_variant_id"
  end

  create_table "orders", force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "client_id", null: false
    t.decimal "total_price", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.datetime "transaction_created_at", null: false
    t.index ["account_id"], name: "index_orders_on_account_id"
  end

  create_table "products", force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "category_id", null: false
    t.text "title", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["account_id"], name: "index_products_on_account_id"
  end

  create_table "variants", force: :cascade do |t|
    t.integer "account_id", null: false
    t.integer "product_id", null: false
    t.text "title"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["account_id"], name: "index_variants_on_account_id"
    t.index ["product_id"], name: "index_variants_on_product_id"
  end

  add_foreign_key "categories", "accounts"
  add_foreign_key "order_lines", "accounts"
  add_foreign_key "order_lines", "orders"
  add_foreign_key "order_lines", "products"
  add_foreign_key "order_lines", "variants"
  add_foreign_key "products", "accounts"
  add_foreign_key "variants", "accounts"
  add_foreign_key "variants", "accounts"
  add_foreign_key "variants", "products"
end
