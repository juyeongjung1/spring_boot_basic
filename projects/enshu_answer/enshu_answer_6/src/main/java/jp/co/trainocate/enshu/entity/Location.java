package jp.co.trainocate.enshu.entity;

import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import lombok.Data;

//演習6.1-a 正解
@Entity
@Table(name = "location")
@Data
public class Location {

  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY) // 自動採番
  private Integer id;

  @Column
  private String name;

  
//演習6.1-c 正解
  @OneToMany(mappedBy = "location")
  private List<Employee> employeeList;
  //ゲッター・セッター（省略可）
  
  
}
