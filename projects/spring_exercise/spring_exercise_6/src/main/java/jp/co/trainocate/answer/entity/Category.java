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
@Table(name = "category")
public class Category {
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	@Column(length = 30)
	private String name;

	//ここに、「1対多」の参照関係を表現するために、
	//List<Product>型の、productListのフィールドを追記してください。
	//その後、1対多の関係を表現するアノテーションを付与してください。
	/*@OneToMany(mappedBy = "category")
	private List<Product> productList;*/
}