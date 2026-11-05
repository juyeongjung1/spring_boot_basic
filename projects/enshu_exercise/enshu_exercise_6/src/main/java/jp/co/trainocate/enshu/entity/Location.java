package jp.co.trainocate.enshu.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import lombok.Data;

//演習6.1-a 正解


//演習6.1-a
//Locationエンティティを確認してください。
//・id: 主キー、自動採番
//・name: null禁止
@Entity
@Table(name = "location")
@Data
public class Location {

	//ここにアノテーションを追記してください。
	 @Id
	  @GeneratedValue(strategy = GenerationType.IDENTITY) // 自動採番
	  private Integer id;

	  @Column
	  private String name;

  
//演習6.1-c
  //この下に、Locationが参照元となるリスト型のフィールドを追加してください。
  //リスト名は employeeList としてください。
  //アノテーション(@OneToMany)も忘れずに記述してください。
}
