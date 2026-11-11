package jp.co.trainocate.answer.form;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Size;
import lombok.Data;

@Data
public class ProductForm {
    private Integer id; // 商品番号

    @NotBlank(message = "商品名を入力してください。")
    @Size(max = 30,
            message = "商品名は30文字以内で入力してください。")
    private String name; // 商品名

    @NotNull(message = "価格を入力してください。")
    @Min(value = 0, message = "価格は0円以上で入力してください。")
    private Integer price; // 商品価格

    @NotNull(message = "カテゴリを選択してください。")
    private Integer categoryId; // カテゴリID
}
