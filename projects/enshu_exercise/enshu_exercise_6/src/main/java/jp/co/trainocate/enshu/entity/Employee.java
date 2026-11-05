package jp.co.trainocate.enshu.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;

@Entity
@Data
public class Employee {
	
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column
	private String password;
	@Column
	private String name;
	@Column
	private Integer salary;
	
	//演習6.1-b
    //Location型のフィールドを追加してください。
    //リレーション設定（@ManyToOne）と外部参照設定（@JoinColumn）も忘れずに記述してください。

	
	//演習6.5-d
	//locationIdのフィールドを追加してください。
	//@JoinColumn に insertable = false, updatable = falseを付けることも大事です。
	
}
