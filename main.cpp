#include <boost/json.hpp>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <string_view>
#include <vector>

namespace {

size_t getFileSize(std::string_view fileName)
{
    std::error_code ec{};
    const auto size = std::filesystem::file_size(fileName, ec);
    if (ec) {
        std::terminate();
    }
    return size;
}

std::string readFileToString(std::string_view fileName)
{
    const auto fileSize = getFileSize(fileName);
    if (fileSize == 0) {
        return std::string{};
    }
    std::filebuf file;
    if (!file.open(std::filesystem::path(fileName), std::ios_base::in | std::ios_base::binary)) {
        std::terminate();
    }
    std::string result(fileSize, '\0');
    const auto read =
        file.sgetn(reinterpret_cast<char*>(&result[0]), static_cast<std::streamsize>(fileSize));
    if (static_cast<size_t>(read) != fileSize) {
        std::terminate();
    }
    return result;
}

void checkAllFields(const boost::json::value& value)
{
    const std::vector<std::string_view> names = {
        "x_offset", "y_offset", "radius", "vux", "vuy", "vlx", "vly"};
    if (value.is_object()) {
        const auto& obj = value.get_object();
        for (const auto& [name, val]: obj) {
            if (val.is_object() || val.is_array()) {
                checkAllFields(val);
            } else if (std::find(names.cbegin(), names.cend(), name) != names.cend()) {
                std::cout << name << " = " << val.as_double() << std::endl;
            }
        }
    } else if (value.is_array()) {
        const auto& arr = value.get_array();
        for (const auto& el: arr) {
            checkAllFields(el);
        }
    }
}

} // namespace

int main(int argc, char* argv[])
{
    std::string filename;
    if (argc == 2) {
        filename = argv[1];
    } else {
        std::cout << "Input filename: ";
        std::cin >> filename;
    }
    boost::json::parse_options opt;
    opt.allow_comments = true;
    opt.allow_trailing_commas = true;
    opt.allow_infinity_and_nan = true;
    const auto json = boost::json::parse(readFileToString(filename), {}, opt);
    checkAllFields(json);
    return 0;
}
