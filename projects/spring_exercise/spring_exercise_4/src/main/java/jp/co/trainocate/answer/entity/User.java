package jp.co.trainocate.answer.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.Data;

@Data
@Entity
@Table(name = "user")
public class User {
	
	@Id
    private Integer empId;

    @Column(length = 15, nullable = false)
    private String password;

    @Column(name = "emp_name", length = 30, nullable = false)
    private String empName;
}
