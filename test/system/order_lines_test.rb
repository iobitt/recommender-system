require "application_system_test_case"

class OrderLinesTest < ApplicationSystemTestCase
  setup do
    @order_line = order_lines(:one)
  end

  test "visiting the index" do
    visit order_lines_url
    assert_selector "h1", text: "Order lines"
  end

  test "should create order line" do
    visit order_lines_url
    click_on "New order line"

    fill_in "Account", with: @order_line.account_id
    fill_in "Order", with: @order_line.order_id
    fill_in "Product", with: @order_line.product_id
    fill_in "Quantity", with: @order_line.quantity
    fill_in "Title", with: @order_line.title
    fill_in "Variant", with: @order_line.variant_id
    click_on "Create Order line"

    assert_text "Order line was successfully created"
    click_on "Back"
  end

  test "should update Order line" do
    visit order_line_url(@order_line)
    click_on "Edit this order line", match: :first

    fill_in "Account", with: @order_line.account_id
    fill_in "Order", with: @order_line.order_id
    fill_in "Product", with: @order_line.product_id
    fill_in "Quantity", with: @order_line.quantity
    fill_in "Title", with: @order_line.title
    fill_in "Variant", with: @order_line.variant_id
    click_on "Update Order line"

    assert_text "Order line was successfully updated"
    click_on "Back"
  end

  test "should destroy Order line" do
    visit order_line_url(@order_line)
    click_on "Destroy this order line", match: :first

    assert_text "Order line was successfully destroyed"
  end
end
