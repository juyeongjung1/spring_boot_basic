package jp.co.trainocate.answer.form;

import lombok.Data;

@Data
public class ProductForm {
	private Integer id; //商品番号
	private String name; //商品名
	private Integer price; //商品価格
	
	private Integer categoryId; //カテゴリID
}
