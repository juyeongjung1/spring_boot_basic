package jp.co.trainocate.answer.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Entity
@Data
@Table(name = "product")

public class Product {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	@Column(length = 30, nullable = false)
	private String name;

	@Column(nullable = false)
	private Integer price;

	//【ここに、category_idの代わりに、正しいフィールドを定義してください。】
	//【その後、多対1の関係を表現するアノテーションを付与してください。】
	
	/*@ManyToOne
	@JoinColumn(name = "category_id")*/
	//private Category category;
	
	//【登録・更新実装時は、追加のフィールドの「category_idを追加し、
	//@JoinColumn に insertable = false, updatable = falseを付ける必要があります。】

}