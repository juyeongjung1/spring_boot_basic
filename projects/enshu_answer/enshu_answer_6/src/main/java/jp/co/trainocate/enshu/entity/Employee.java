package jp.co.trainocate.enshu.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
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
	
	//演習6.1-b 正解
	/* @ManyToOne
	@JoinColumn(name = "location_id") // 外部キー列
	private Location location;*/
    
  //演習6.5-d 正解
	@ManyToOne
    @JoinColumn(name = "location_id", insertable = false, updatable = false)
    private Location location;
    
    @Column(name = "location_id")
    private Integer locationId;
}
